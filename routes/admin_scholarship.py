"""
Admin Scholarship Routes
Handles scholarship management and approval
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, User, Department, Scholarship
from extensions import db
from routes.email_utils import send_scholarship_approval_email

admin_scholarship_bp = Blueprint('admin_scholarship', __name__, url_prefix='/admin')



@admin_scholarship_bp.route('/scholarships')
@login_required
def admin_scholarships():
    """Admin scholarships page - displays eligible students for scholarships"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_scholarship.dashboard'))
    
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


@admin_scholarship_bp.route('/scholarship/<student_id>')
@login_required
def admin_view_scholarship(student_id):
    """Admin view for individual student scholarship details"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_scholarship.dashboard'))
    
    # Convert student_id to int
    student_id = int(student_id)
    
    # Get student
    student = User.query.filter_by(student_id=student_id).first()
    
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('admin_scholarship.admin_scholarships'))
    
    # Check if student is from admin's department
    if student.dept_id != current_user.dept_id:
        flash('Access denied. You can only view students from your department.', 'danger')
        return redirect(url_for('admin_scholarship.admin_scholarships'))
    
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


@admin_scholarship_bp.route('/scholarship/approve/<student_id>', methods=['POST'])
@login_required
def approve_scholarship(student_id):
    """Approve scholarship for a student"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Convert student_id to int
    student_id = int(student_id)
    
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
    
    # Send email notification
    try:
        send_scholarship_approval_email(
            student.email,
            student.name,
            scholarship_type,
            scholarship_amount,
            semester_name
        )
    except Exception as e:
        print(f"Failed to send email to {student.email}: {str(e)}")
    
    return jsonify({
        'success': True,
        'message': 'Scholarship approved successfully',
        'remaining_budget': department.budget
    })


@admin_scholarship_bp.route('/scholarship/approve-all', methods=['POST'])
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
                    
                    # Send email notification
                    try:
                        send_scholarship_approval_email(
                            student.email,
                            student.name,
                            scholarship_type,
                            scholarship_amount,
                            semester_name
                        )
                    except Exception as e:
                        print(f"Failed to send email to {student.email}: {str(e)}")
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{approved_count} scholarships approved successfully',
        'approved_count': approved_count,
        'total_amount': total_amount,
        'remaining_budget': department.budget
    })


@admin_scholarship_bp.route('/scholarship/approve-multiple', methods=['POST'])
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
        
        # Send email notification
        try:
            send_scholarship_approval_email(
                student.email,
                student.name,
                scholarship_type,
                scholarship_amount,
                semester_name
            )
        except Exception as e:
            print(f"Failed to send email to {student.email}: {str(e)}")
    
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


@admin_scholarship_bp.route('/scholarships/view')
@login_required
def admin_view_scholarships():
    """Admin view scholarships page - displays all awarded scholarships"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_scholarship.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get all awarded scholarships for students in this department
    scholarships = db.session.query(Scholarship, User).join(
        User, Scholarship.student_id == User.student_id
    ).filter(User.dept_id == current_user.dept_id).order_by(Scholarship.awarded_at.desc()).all()
    
    return render_template('admin_scholarships_view.html',
                         admin=current_user,
                         department=department,
                         scholarships=scholarships)


