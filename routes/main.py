"""
Main Routes
Handles home, dashboard, and other general routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, User, Department, Scholarship, Stipend, IncomeRecord, Application
from extensions import db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Home page - redirect to login if not authenticated"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('home.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - displays student information"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('main.admin_dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    return render_template('dashboard.html', 
                         user=current_user, 
                         department=department,
                         academic_record=academic_record)


@main_bp.route('/scholarships')
@login_required
def student_scholarships():
    """Student scholarships page - displays awarded scholarships or eligibility message"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('main.admin_scholarships'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    # Check eligibility based on LAST COMPLETED semester GPA
    is_eligible = False
    last_semester_gpa = None
    last_completed_semester = None
    has_current_award = False
    ineligibility_reason = None
    
    if academic_record:
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        
        # Awards are for the last completed semester
        semester_name = f"Semester {last_completed_semester}" if last_completed_semester > 0 else None
        
        if not semester_name or last_completed_semester <= 0:
            ineligibility_reason = 'first_semester'
        else:
            # Check if already received scholarship or stipend for last completed semester
            existing_scholarship = Scholarship.query.filter_by(
                student_id=current_user.student_id,
                semester=semester_name
            ).first()
            
            existing_stipend = Stipend.query.filter_by(
                student_id=current_user.student_id,
                semester=semester_name
            ).first()
            
            if existing_scholarship:
                has_current_award = True
                ineligibility_reason = 'scholarship'
            elif existing_stipend:
                has_current_award = True
                ineligibility_reason = 'stipend'
            elif last_semester_gpa and last_semester_gpa >= 3.8:
                is_eligible = True
            elif last_semester_gpa and last_semester_gpa >= 3.5:
                ineligibility_reason = 'low_gpa_stipend'
            else:
                ineligibility_reason = 'low_gpa'
    
    # Get scholarships awarded to this student
    scholarships = Scholarship.query.filter_by(student_id=current_user.student_id).order_by(Scholarship.awarded_at.desc()).all()
    
    return render_template('student_scholarships.html',
                         user=current_user,
                         academic_record=academic_record,
                         is_eligible=is_eligible,
                         has_current_award=has_current_award,
                         ineligibility_reason=ineligibility_reason,
                         scholarships=scholarships,
                         last_semester_gpa=last_semester_gpa,
                         last_completed_semester=last_completed_semester)


@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard - displays admin information and analytics"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # --- Analytics Data Gathering ---
    
    # 1. Student Stats
    students = User.query.filter_by(dept_id=current_user.dept_id).all()
    total_students = len(students)
    
    # 2. GPA Distribution
    gpas = []
    academic_records = db.session.query(AcademicRecord).select_from(User).join(AcademicRecord, User.student_id == AcademicRecord.student_id).filter(User.dept_id == current_user.dept_id).all()
    for record in academic_records:
        current_gpa = record.get_current_gpa()
        if current_gpa:
            gpas.append(current_gpa)
            
    # 3. Scholarship & Stipend Counts
    scholarship_count = db.session.query(Scholarship).select_from(User).join(Scholarship, User.student_id == Scholarship.student_id).filter(User.dept_id == current_user.dept_id).count()
    stipend_count = db.session.query(Stipend).select_from(User).join(Stipend, User.student_id == Stipend.student_id).filter(User.dept_id == current_user.dept_id).count()
    
    # 4. Budget Stats
    initial_budget = 200000.0 # Assuming initial budget is constant or stored somewhere else, using hardcoded for now based on schema
    # Better approach: Calculate spent amount
    spent_scholarships = db.session.query(db.func.sum(Scholarship.amount)).select_from(User).join(Scholarship, User.student_id == Scholarship.student_id).filter(User.dept_id == current_user.dept_id).scalar() or 0
    spent_stipends = db.session.query(db.func.sum(Stipend.amount)).select_from(User).join(Stipend, User.student_id == Stipend.student_id).filter(User.dept_id == current_user.dept_id).scalar() or 0
    total_spent = spent_scholarships + spent_stipends
    remaining_budget = department.budget
    
    # --- Plot Generation ---
    
    # Plot 1: GPA Distribution (Histogram)
    plt.figure(figsize=(6, 4))
    plt.hist(gpas, bins=10, color='#4caf50', edgecolor='black', alpha=0.7)
    plt.title('Student GPA Distribution')
    plt.xlabel('GPA')
    plt.ylabel('Number of Students')
    plt.grid(axis='y', alpha=0.5)
    
    img1 = io.BytesIO()
    plt.savefig(img1, format='png', bbox_inches='tight')
    img1.seek(0)
    plot_gpa = base64.b64encode(img1.getvalue()).decode()
    plt.close()
    
    # Plot 2: Budget Utilization (Pie Chart)
    plt.figure(figsize=(6, 4))
    labels = ['Remaining', 'Scholarships', 'Stipends']
    sizes = [remaining_budget, spent_scholarships, spent_stipends]
    colors = ['#e0e0e0', '#4caf50', '#2196f3']
    explode = (0.1, 0, 0) 
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Budget Utilization')
    
    img2 = io.BytesIO()
    plt.savefig(img2, format='png', bbox_inches='tight')
    img2.seek(0)
    plot_budget = base64.b64encode(img2.getvalue()).decode()
    plt.close()
    
    # Plot 3: Awards Count (Bar Chart)
    plt.figure(figsize=(6, 4))
    categories = ['Scholarships', 'Stipends']
    counts = [scholarship_count, stipend_count]
    plt.bar(categories, counts, color=['#4caf50', '#2196f3'])
    plt.title('Total Awards Granted')
    plt.ylabel('Count')
    
    img3 = io.BytesIO()
    plt.savefig(img3, format='png', bbox_inches='tight')
    img3.seek(0)
    plot_awards = base64.b64encode(img3.getvalue()).decode()
    plt.close()

    return render_template('admin_dashboard.html',
                         admin=current_user,
                         department=department,
                         stats={
                             'total_students': total_students,
                             'avg_gpa': round(sum(gpas)/len(gpas), 2) if gpas else 0,
                             'scholarship_count': scholarship_count,
                             'stipend_count': stipend_count,
                             'total_spent': total_spent
                         },
                         plots={
                             'gpa': plot_gpa,
                             'budget': plot_budget,
                             'awards': plot_awards
                         })


@main_bp.route('/admin/students')
@login_required
def admin_students():
    """Admin students page - displays and searches students from admin's department"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get search query
    search_query = request.args.get('search', '').strip()
    
    # Base query for students in admin's department
    students_query = User.query.filter_by(dept_id=current_user.dept_id)
    
    # Apply search filter if provided
    if search_query:
        students_query = students_query.filter(
            db.or_(
                User.name.ilike(f'%{search_query}%'),
                User.email.ilike(f'%{search_query}%'),
                User.student_id.like(f'%{search_query}%'),
                User.reg_no.like(f'%{search_query}%'),
                User.session.ilike(f'%{search_query}%')
            )
        )
    
    # Get all students
    students = students_query.order_by(User.student_id).all()
    
    return render_template('admin_students.html',
                         admin=current_user,
                         students=students,
                         search_query=search_query)


@main_bp.route('/admin/student/<int:student_id>')
@login_required
def admin_view_student(student_id):
    """Admin view for individual student details"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get student
    student = User.query.filter_by(student_id=student_id).first()
    
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('main.admin_students'))
    
    # Check if student is from admin's department
    if student.dept_id != current_user.dept_id:
        flash('Access denied. You can only view students from your department.', 'danger')
        return redirect(url_for('main.admin_students'))
    
    # Get student's department and academic record
    department = student.get_department()
    academic_record = AcademicRecord.query.filter_by(student_id=student.student_id).first()
    
    return render_template('admin_student_detail.html',
                         admin=current_user,
                         student=student,
                         department=department,
                         academic_record=academic_record)


@main_bp.route('/admin/student/<int:student_id>/academic-record/update', methods=['POST'])
@login_required
def update_academic_record(student_id):
    """Update student's academic record"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get student
    student = User.query.filter_by(student_id=student_id).first()
    
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Check if student is from admin's department
    if student.dept_id != current_user.dept_id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get data from request
    data = request.get_json()
    current_semester = data.get('current_semester')
    semester_gpas = data.get('semester_gpas', {})
    
    # Validate inputs
    if current_semester is None:
        return jsonify({'success': False, 'message': 'Missing current semester'}), 400
    
    try:
        current_semester = int(current_semester)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid current semester value'}), 400
    
    # Validate current semester range
    if current_semester < 1 or current_semester > 8:
        return jsonify({'success': False, 'message': 'Current semester must be between 1 and 8'}), 400
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=student_id).first()
    
    if not academic_record:
        return jsonify({'success': False, 'message': 'Academic record not found'}), 404
    
    # Update current semester
    academic_record.current_semester = current_semester
    
    # Update semester GPAs
    for sem_num, gpa_value in semester_gpas.items():
        try:
            sem_num = int(sem_num)
            if gpa_value is not None and gpa_value != '':
                gpa_value = float(gpa_value)
                
                # Validate GPA range
                if gpa_value < 0 or gpa_value > 4:
                    return jsonify({'success': False, 'message': f'Semester {sem_num} GPA must be between 0.00 and 4.00'}), 400
                
                setattr(academic_record, f'semester_{sem_num}_gpa', gpa_value)
            else:
                setattr(academic_record, f'semester_{sem_num}_gpa', None)
        except (ValueError, AttributeError):
            return jsonify({'success': False, 'message': f'Invalid GPA value for semester {sem_num}'}), 400
    
    # Auto-calculate CGPA
    academic_record.cgpa = academic_record.calculate_cgpa()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Academic record updated successfully',
        'cgpa': academic_record.cgpa
    })


@main_bp.route('/admin/scholarships')
@login_required
def admin_scholarships():
    """Admin scholarships page - displays eligible students for scholarships"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get all students from admin's department with their academic records
    students = db.session.query(User, AcademicRecord).join(
        AcademicRecord, User.student_id == AcademicRecord.student_id
    ).filter(User.dept_id == current_user.dept_id).all()
    
    # Filter eligible students and calculate scholarship amounts based on LAST COMPLETED semester
    eligible_students = []
    total_scholarship_amount = 0
    
    for student, academic_record in students:
        scholarship_type = None
        scholarship_amount = 0
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        
        # Skip if no completed semester yet
        if last_completed_semester <= 0:
            continue
        
        # Check eligibility based on LAST COMPLETED semester GPA
        if last_semester_gpa and last_semester_gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif last_semester_gpa and last_semester_gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
        
        # Only add if eligible
        if scholarship_type:
            # Check if already awarded for the last completed semester
            semester_name = f"Semester {last_completed_semester}"
            existing_scholarship = Scholarship.query.filter_by(
                student_id=student.student_id,
                semester=semester_name
            ).first()
            
            if not existing_scholarship:
                eligible_students.append({
                    'student': student,
                    'academic_record': academic_record,
                    'scholarship_type': scholarship_type,
                    'scholarship_amount': scholarship_amount,
                    'last_semester_gpa': last_semester_gpa,
                    'last_completed_semester': last_completed_semester
                })
                total_scholarship_amount += scholarship_amount
    
    # Sort eligible students by last semester GPA in descending order (highest first)
    eligible_students.sort(key=lambda x: x['last_semester_gpa'] or 0, reverse=True)
    
    return render_template('admin_scholarships.html',
                         admin=current_user,
                         department=department,
                         eligible_students=eligible_students,
                         total_scholarship_amount=total_scholarship_amount)


@main_bp.route('/admin/scholarship/<int:student_id>')
@login_required
def admin_view_scholarship(student_id):
    """Admin view for individual student scholarship details"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get student
    student = User.query.filter_by(student_id=student_id).first()
    
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('main.admin_scholarships'))
    
    # Check if student is from admin's department
    if student.dept_id != current_user.dept_id:
        flash('Access denied. You can only view students from your department.', 'danger')
        return redirect(url_for('main.admin_scholarships'))
    
    # Get student's department and academic record
    department = student.get_department()
    academic_record = AcademicRecord.query.filter_by(student_id=student.student_id).first()
    
    # Calculate scholarship eligibility based on LAST COMPLETED semester
    scholarship_type = None
    scholarship_amount = 0
    last_semester_gpa = None
    last_completed_semester = None
    
    if academic_record:
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        if last_semester_gpa and last_semester_gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif last_semester_gpa and last_semester_gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
    
    return render_template('admin_scholarship_detail.html',
                         admin=current_user,
                         student=student,
                         department=department,
                         academic_record=academic_record,
                         scholarship_type=scholarship_type,
                         scholarship_amount=scholarship_amount,
                         last_semester_gpa=last_semester_gpa,
                         last_completed_semester=last_completed_semester)


@main_bp.route('/admin/scholarship/approve/<int:student_id>', methods=['POST'])
@login_required
def approve_scholarship(student_id):
    """Approve scholarship for a student"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get student
    student = User.query.filter_by(student_id=student_id).first()
    
    if not student or student.dept_id != current_user.dept_id:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=student_id).first()
    
    if not academic_record:
        return jsonify({'success': False, 'message': 'Academic record not found'}), 404
    
    # Calculate scholarship based on LAST COMPLETED semester
    scholarship_type = None
    scholarship_amount = 0
    last_semester_gpa = academic_record.get_last_semester_gpa()
    last_completed_semester = academic_record.get_last_completed_semester()
    
    if last_completed_semester <= 0:
        return jsonify({'success': False, 'message': 'Student has no completed semester'}), 400
    
    if last_semester_gpa and last_semester_gpa >= 3.9:
        scholarship_type = "Chancellor Scholarship"
        scholarship_amount = 15000
    elif last_semester_gpa and last_semester_gpa >= 3.8:
        scholarship_type = "BUP Scholarship"
        scholarship_amount = 9000
    else:
        return jsonify({'success': False, 'message': 'Student not eligible'}), 400
    
    # Check if already awarded for last completed semester
    semester_name = f"Semester {last_completed_semester}"
    existing_scholarship = Scholarship.query.filter_by(
        student_id=student_id,
        semester=semester_name
    ).first()
    
    if existing_scholarship:
        return jsonify({'success': False, 'message': 'Scholarship already awarded'}), 400
    
    # Check department budget
    department = current_user.get_department()
    if department.budget < scholarship_amount:
        return jsonify({'success': False, 'message': 'Insufficient department budget'}), 400
    
    # Create scholarship
    scholarship = Scholarship(
        student_id=student_id,
        student_name=student.name,
        type=scholarship_type,
        amount=scholarship_amount,
        semester=semester_name
    )
    
    # Update department budget
    department.budget -= scholarship_amount
    
    db.session.add(scholarship)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Scholarship approved successfully',
        'remaining_budget': department.budget
    })


@main_bp.route('/admin/scholarship/approve-all', methods=['POST'])
@login_required
def approve_all_scholarships():
    """Approve all eligible scholarships"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get department info
    department = current_user.get_department()
    
    # Get all students from admin's department with their academic records
    students = db.session.query(User, AcademicRecord).join(
        AcademicRecord, User.student_id == AcademicRecord.student_id
    ).filter(User.dept_id == current_user.dept_id).all()
    
    approved_count = 0
    total_amount = 0
    
    for student, academic_record in students:
        scholarship_type = None
        scholarship_amount = 0
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        
        # Skip if no completed semester
        if last_completed_semester <= 0:
            continue
        
        # Check eligibility based on LAST COMPLETED semester GPA
        if last_semester_gpa and last_semester_gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif last_semester_gpa and last_semester_gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
        
        # Only process if eligible
        if scholarship_type:
            # Check if already awarded for the last completed semester
            semester_name = f"Semester {last_completed_semester}"
            existing_scholarship = Scholarship.query.filter_by(
                student_id=student.student_id,
                semester=semester_name
            ).first()
            
            if not existing_scholarship:
                # Check if we have enough budget
                if department.budget >= scholarship_amount:
                    # Create scholarship
                    scholarship = Scholarship(
                        student_id=student.student_id,
                        student_name=student.name,
                        type=scholarship_type,
                        amount=scholarship_amount,
                        semester=semester_name
                    )
                    
                    # Update department budget
                    department.budget -= scholarship_amount
                    total_amount += scholarship_amount
                    
                    db.session.add(scholarship)
                    approved_count += 1
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{approved_count} scholarships approved successfully',
        'approved_count': approved_count,
        'total_amount': total_amount,
        'remaining_budget': department.budget
    })


@main_bp.route('/admin/scholarship/approve-multiple', methods=['POST'])
@login_required
def approve_multiple_scholarships():
    """Approve multiple selected scholarships"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get student IDs from request
    data = request.get_json()
    student_ids = data.get('studentIds', [])
    
    if not student_ids:
        return jsonify({'success': False, 'message': 'No students selected'}), 400
    
    # Get department info
    department = current_user.get_department()
    
    approved_count = 0
    total_amount = 0
    failed_students = []
    
    for student_id in student_ids:
        # Get student
        student = User.query.filter_by(student_id=student_id).first()
        
        if not student or student.dept_id != current_user.dept_id:
            failed_students.append(f"Student {student_id}: Not found or wrong department")
            continue
        
        # Get academic record
        academic_record = AcademicRecord.query.filter_by(student_id=student_id).first()
        
        if not academic_record:
            failed_students.append(f"Student {student_id}: No academic record")
            continue
        
        # Calculate scholarship based on LAST COMPLETED semester
        scholarship_type = None
        scholarship_amount = 0
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        
        if last_completed_semester <= 0:
            failed_students.append(f"Student {student_id}: No completed semester")
            continue
        
        if last_semester_gpa and last_semester_gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif last_semester_gpa and last_semester_gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
        else:
            failed_students.append(f"Student {student_id}: Not eligible")
            continue
        
        # Check if already awarded for last completed semester
        semester_name = f"Semester {last_completed_semester}"
        existing_scholarship = Scholarship.query.filter_by(
            student_id=student_id,
            semester=semester_name
        ).first()
        
        if existing_scholarship:
            failed_students.append(f"Student {student_id}: Already awarded")
            continue
        
        # Check department budget
        if department.budget < scholarship_amount:
            failed_students.append(f"Student {student_id}: Insufficient budget")
            continue
        
        # Create scholarship
        scholarship = Scholarship(
            student_id=student_id,
            student_name=student.name,
            type=scholarship_type,
            amount=scholarship_amount,
            semester=semester_name
        )
        
        # Update department budget
        department.budget -= scholarship_amount
        total_amount += scholarship_amount
        
        db.session.add(scholarship)
        approved_count += 1
    
    db.session.commit()
    
    message = f'{approved_count} scholarship(s) approved successfully'
    if failed_students:
        message += f'. {len(failed_students)} failed.'
    
    return jsonify({
        'success': True,
        'message': message,
        'approved_count': approved_count,
        'total_amount': total_amount,
        'remaining_budget': department.budget,
        'failed_students': failed_students
    })


@main_bp.route('/stipends')
@login_required
def student_stipends():
    """Student stipends page - displays eligibility, application form and history"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('main.admin_dashboard'))
    
    eligibility_criteria = [
        "Complete at least one semester.",
        "Maintain a minimum GPA of 3.50 in the last completed semester.",
        "No scholarship or stipend can be taken for the same semester.",
        "Vice Chancellor Stipend needs GPA ≥ 3.75."
    ]

    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    # Check eligibility based on LAST COMPLETED semester GPA
    is_eligible = False
    eligible_for_vc = False
    last_semester_gpa = None
    last_completed_semester = None
    ineligibility_reason = None
    
    if academic_record:
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        
        # Awards are for the last completed semester
        semester_name = f"Semester {last_completed_semester}" if last_completed_semester > 0 else None
        
        if not semester_name or last_completed_semester <= 0:
            ineligibility_reason = 'first_semester'
        else:
            # Check if already received scholarship or stipend for last completed semester
            existing_scholarship = Scholarship.query.filter_by(
                student_id=current_user.student_id,
                semester=semester_name
            ).first()
            
            existing_stipend = Stipend.query.filter_by(
                student_id=current_user.student_id,
                semester=semester_name
            ).first()
            
            # Check eligibility and set reason if not eligible
            if existing_scholarship:
                ineligibility_reason = 'scholarship'
            elif existing_stipend:
                ineligibility_reason = 'stipend'
            elif last_semester_gpa and last_semester_gpa >= 3.5:
                is_eligible = True
                # Check if eligible for Vice Chancellor Stipend
                if last_semester_gpa >= 3.75:
                    eligible_for_vc = True
            else:
                ineligibility_reason = 'low_gpa'
    
    # Get pending application
    pending_application = Application.query.filter_by(
        student_id=current_user.student_id,
        status='Pending'
    ).first()

    # Check if already has award for last completed semester
    has_current_semester_scholarship = None
    has_current_semester_stipend = None
    if last_completed_semester and last_completed_semester > 0:
        semester_name = f"Semester {last_completed_semester}"
        has_current_semester_scholarship = Scholarship.query.filter_by(
            student_id=current_user.student_id,
            semester=semester_name
        ).first()
        has_current_semester_stipend = Stipend.query.filter_by(
            student_id=current_user.student_id,
            semester=semester_name
        ).first()

    can_proceed_with_application = (
        bool(last_completed_semester and last_completed_semester > 0)
        and not has_current_semester_scholarship
        and not has_current_semester_stipend
        and is_eligible
        and pending_application is None
    )
    
    # Get application history
    applications = Application.query.filter_by(student_id=current_user.student_id).order_by(Application.created_at.desc()).all()
    
    # Get awarded stipends
    stipends = Stipend.query.filter_by(student_id=current_user.student_id).order_by(Stipend.awarded_at.desc()).all()
    
    # Get awarded scholarships (to show in stipend page as well)
    scholarships = Scholarship.query.filter_by(student_id=current_user.student_id).order_by(Scholarship.awarded_at.desc()).all()
    
    return render_template('student_stipends.html',
                         user=current_user,
                         academic_record=academic_record,
                         is_eligible=is_eligible,
                         eligible_for_vc=eligible_for_vc,
                         ineligibility_reason=ineligibility_reason,
                         pending_application=pending_application,
                         can_proceed_with_application=can_proceed_with_application,
                         applications=applications,
                         stipends=stipends,
                         scholarships=scholarships,
                         has_current_semester_scholarship=has_current_semester_scholarship,
                         has_current_semester_stipend=has_current_semester_stipend,
                         last_semester_gpa=last_semester_gpa,
                         last_completed_semester=last_completed_semester,
                         eligibility_criteria=eligibility_criteria)


@main_bp.route('/stipends/apply', methods=['POST'])
@login_required
def apply_stipend():
    """Handle stipend application submission"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('main.admin_dashboard'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    # Check eligibility again based on LAST COMPLETED semester
    last_semester_gpa = academic_record.get_last_semester_gpa() if academic_record else None
    last_completed_semester = academic_record.get_last_completed_semester() if academic_record else 0
    
    if last_completed_semester <= 0:
        flash('You are not eligible for a stipend. No completed semester found.', 'danger')
        return redirect(url_for('main.student_stipends'))
    
    if not last_semester_gpa or last_semester_gpa < 3.5:
        flash('You are not eligible for a stipend. Minimum GPA required is 3.5', 'danger')
        return redirect(url_for('main.student_stipends'))
    
    # Check if already received scholarship or stipend for last completed semester
    semester_name = f"Semester {last_completed_semester}"
    existing_scholarship = Scholarship.query.filter_by(
        student_id=current_user.student_id,
        semester=semester_name
    ).first()
    
    existing_stipend = Stipend.query.filter_by(
        student_id=current_user.student_id,
        semester=semester_name
    ).first()
    
    if existing_scholarship or existing_stipend:
        flash('You have already received a scholarship or stipend for this semester.', 'warning')
        return redirect(url_for('main.student_stipends'))
    
    # Check for pending application
    pending_application = Application.query.filter_by(
        student_id=current_user.student_id,
        status='Pending'
    ).first()
    
    if pending_application:
        flash('You already have a pending application.', 'warning')
        return redirect(url_for('main.student_stipends'))
    
    # Get form data
    amount = request.form.get('amount')
    source = request.form.get('source')
    family_member = request.form.get('family_member')
    stipend_type = request.form.get('stipend_type')
    
    if not amount or not source or not family_member or not stipend_type:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('main.student_stipends'))
    
    # Validate stipend type based on GPA
    if stipend_type == "Vice Chancellor Stipend" and last_semester_gpa < 3.75:
        flash('You are not eligible for Vice Chancellor Stipend. Minimum GPA required is 3.75', 'danger')
        return redirect(url_for('main.student_stipends'))
    
    if stipend_type not in ["BUP Stipend", "Vice Chancellor Stipend"]:
        flash('Invalid stipend type selected.', 'danger')
        return redirect(url_for('main.student_stipends'))
    
    try:
        amount = float(amount)
        family_member = int(family_member)
    except ValueError:
        flash('Invalid input values.', 'danger')
        return redirect(url_for('main.student_stipends'))
    
    # Check if income record exists for this student, update it or create new one
    income_record = IncomeRecord.query.filter_by(student_id=current_user.student_id).first()
    
    if income_record:
        # Update existing record
        income_record.amount = amount
        income_record.source = source
        income_record.family_member = family_member
    else:
        # Create new Income Record
        income_record = IncomeRecord(
            student_id=current_user.student_id,
            amount=amount,
            source=source,
            family_member=family_member
        )
        db.session.add(income_record)
    
    # Create Application
    application = Application(
        student_id=current_user.student_id,
        type=stipend_type,
        semester=semester_name,
        status='Pending'
    )
    
    db.session.add(application)
    db.session.commit()
    
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('main.student_stipends'))


@main_bp.route('/admin/stipends/applications')
@login_required
def admin_stipend_applications():
    """Admin view for pending stipend applications"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get pending applications for students in admin's department
    applications = db.session.query(Application).join(
        User, Application.student_id == User.student_id
    ).filter(
        User.dept_id == current_user.dept_id,
        Application.status == 'Pending'
    ).all()
    
    applications_data = []
    for app in applications:
        # Get student info
        student = User.query.filter_by(student_id=app.student_id).first()
        
        # Get academic record
        academic_record = AcademicRecord.query.filter_by(student_id=app.student_id).first()
        
        # Get the most recent income record for this student
        income = IncomeRecord.query.filter_by(student_id=app.student_id).order_by(IncomeRecord.date.desc()).first()
        
        amount = 6000
        if app.type == "Vice Chancellor Stipend":
            amount = 12000
            
        applications_data.append({
            'application': app,
            'student': student,
            'academic_record': academic_record,
            'income': income,
            'amount': amount
        })
    
    return render_template('admin_stipend_applications.html',
                         admin=current_user,
                         department=department,
                         applications=applications_data)


@main_bp.route('/admin/stipends/application/<int:application_id>')
@login_required
def admin_stipend_detail(application_id):
    """Admin view for individual stipend application details"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get application
    application = Application.query.get(application_id)
    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('main.admin_stipend_applications'))
    
    # Get student and check if from admin's department
    student = User.query.filter_by(student_id=application.student_id).first()
    if not student or student.dept_id != current_user.dept_id:
        flash('Access denied. You can only view applications from your department.', 'danger')
        return redirect(url_for('main.admin_stipend_applications'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=application.student_id).first()
    
    # Get income record
    income = IncomeRecord.query.filter_by(student_id=application.student_id).order_by(IncomeRecord.date.desc()).first()
    
    # Calculate amount
    amount = 6000
    if application.type == "Vice Chancellor Stipend":
        amount = 12000
    
    # Get last semester GPA
    last_semester_gpa = academic_record.get_last_semester_gpa() if academic_record else None
    last_completed_semester = academic_record.get_last_completed_semester() if academic_record else 0
    
    return render_template('admin_stipend_detail.html',
                         admin=current_user,
                         application=application,
                         student=student,
                         academic_record=academic_record,
                         income=income,
                         amount=amount,
                         last_semester_gpa=last_semester_gpa,
                         last_completed_semester=last_completed_semester)


@main_bp.route('/admin/stipends/approve/<int:application_id>', methods=['POST'])
@login_required
def approve_stipend_application(application_id):
    """Approve a stipend application"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get application
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'success': False, 'message': 'Application not found'}), 404
    
    # Get student to check department
    student = User.query.filter_by(student_id=application.student_id).first()
    if not student or student.dept_id != current_user.dept_id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Determine amount
    amount = 6000
    if application.type == "Vice Chancellor Stipend":
        amount = 12000
    
    # Check budget
    department = current_user.get_department()
    if department.budget < amount:
        return jsonify({'success': False, 'message': 'Insufficient department budget'}), 400
    
    # Create Stipend
    stipend = Stipend(
        student_id=application.student_id,
        student_name=student.name,
        type=application.type,
        amount=amount,
        semester=application.semester
    )
    
    # Update Application status
    application.status = 'Approved'
    
    # Update budget
    department.budget -= amount
    
    db.session.add(stipend)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Application approved successfully'
    })


@main_bp.route('/admin/stipends/reject/<int:application_id>', methods=['POST'])
@login_required
def reject_stipend_application(application_id):
    """Reject a stipend application"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get application
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'success': False, 'message': 'Application not found'}), 404
    
    # Get student to check department
    student = User.query.filter_by(student_id=application.student_id).first()
    if not student or student.dept_id != current_user.dept_id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Update Application status
    application.status = 'Rejected'
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Application rejected'
    })


