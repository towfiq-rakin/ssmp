"""
Main Routes
Handles home, dashboard, and other general routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, User, Department, Scholarship, Stipend
from extensions import db

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
    """Student scholarships/stipends page - displays awarded scholarships, stipends or eligibility message"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('main.admin_scholarships'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    # Check eligibility based on GPA
    is_eligible = False
    eligible_for = None  # 'scholarship', 'stipend', or None
    
    if academic_record:
        if academic_record.gpa >= 3.8:
            is_eligible = True
            eligible_for = 'scholarship'
        elif academic_record.gpa >= 3.5:
            is_eligible = True
            eligible_for = 'stipend'
    
    # Get scholarships and stipends awarded to this student
    scholarships = Scholarship.query.filter_by(student_id=current_user.student_id).order_by(Scholarship.awarded_at.desc()).all()
    stipends = Stipend.query.filter_by(student_id=current_user.student_id).order_by(Stipend.awarded_at.desc()).all()
    
    return render_template('student_scholarships.html',
                         user=current_user,
                         academic_record=academic_record,
                         is_eligible=is_eligible,
                         eligible_for=eligible_for,
                         scholarships=scholarships,
                         stipends=stipends)


@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard - displays admin information"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    return render_template('admin_dashboard.html',
                         admin=current_user,
                         department=department)


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
    cgpa = data.get('cgpa')
    gpa = data.get('gpa')
    semester = data.get('semester')
    
    # Validate inputs
    if cgpa is None or gpa is None or not semester:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    try:
        cgpa = float(cgpa)
        gpa = float(gpa)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid CGPA or GPA value'}), 400
    
    # Validate ranges
    if cgpa < 0 or cgpa > 4:
        return jsonify({'success': False, 'message': 'CGPA must be between 0.00 and 4.00'}), 400
    
    if gpa < 0 or gpa > 4:
        return jsonify({'success': False, 'message': 'GPA must be between 0.00 and 4.00'}), 400
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=student_id).first()
    
    if not academic_record:
        return jsonify({'success': False, 'message': 'Academic record not found'}), 404
    
    # Update academic record
    academic_record.cgpa = cgpa
    academic_record.gpa = gpa
    academic_record.semester = semester
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Academic record updated successfully'
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
    
    # Filter eligible students and calculate scholarship amounts
    eligible_students = []
    total_scholarship_amount = 0
    
    for student, academic_record in students:
        scholarship_type = None
        scholarship_amount = 0
        
        # Check eligibility based on GPA
        if academic_record.gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif academic_record.gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
        
        # Only add if eligible
        if scholarship_type:
            # Check if already awarded for this semester
            existing_scholarship = Scholarship.query.filter_by(
                student_id=student.student_id,
                semester=academic_record.semester
            ).first()
            
            if not existing_scholarship:
                eligible_students.append({
                    'student': student,
                    'academic_record': academic_record,
                    'scholarship_type': scholarship_type,
                    'scholarship_amount': scholarship_amount
                })
                total_scholarship_amount += scholarship_amount
    
    # Sort eligible students by GPA in descending order (highest first)
    eligible_students.sort(key=lambda x: x['academic_record'].gpa, reverse=True)
    
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
    
    # Calculate scholarship eligibility
    scholarship_type = None
    scholarship_amount = 0
    
    if academic_record:
        if academic_record.gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif academic_record.gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
    
    return render_template('admin_scholarship_detail.html',
                         admin=current_user,
                         student=student,
                         department=department,
                         academic_record=academic_record,
                         scholarship_type=scholarship_type,
                         scholarship_amount=scholarship_amount)


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
    
    # Calculate scholarship
    scholarship_type = None
    scholarship_amount = 0
    
    if academic_record.gpa >= 3.9:
        scholarship_type = "Chancellor Scholarship"
        scholarship_amount = 15000
    elif academic_record.gpa >= 3.8:
        scholarship_type = "BUP Scholarship"
        scholarship_amount = 9000
    else:
        return jsonify({'success': False, 'message': 'Student not eligible'}), 400
    
    # Check if already awarded
    existing_scholarship = Scholarship.query.filter_by(
        student_id=student_id,
        semester=academic_record.semester
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
        semester=academic_record.semester
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
        
        # Check eligibility based on GPA
        if academic_record.gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif academic_record.gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
        
        # Only process if eligible
        if scholarship_type:
            # Check if already awarded for this semester
            existing_scholarship = Scholarship.query.filter_by(
                student_id=student.student_id,
                semester=academic_record.semester
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
                        semester=academic_record.semester
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
        
        # Calculate scholarship
        scholarship_type = None
        scholarship_amount = 0
        
        if academic_record.gpa >= 3.9:
            scholarship_type = "Chancellor Scholarship"
            scholarship_amount = 15000
        elif academic_record.gpa >= 3.8:
            scholarship_type = "BUP Scholarship"
            scholarship_amount = 9000
        else:
            failed_students.append(f"Student {student_id}: Not eligible")
            continue
        
        # Check if already awarded
        existing_scholarship = Scholarship.query.filter_by(
            student_id=student_id,
            semester=academic_record.semester
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
            semester=academic_record.semester
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


