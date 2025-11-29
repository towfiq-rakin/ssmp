"""
Admin Stipend Routes
Handles stipend application management and approval
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, User, Department, Stipend, Application, IncomeRecord
from extensions import db

admin_stipend_bp = Blueprint('admin_stipend', __name__, url_prefix='/admin')


@admin_stipend_bp.route('/stipends/applications')
@login_required
def admin_stipend_applications():
    """Admin view for pending stipend applications"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_stipend.dashboard'))
    
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


@admin_stipend_bp.route('/stipends/application/<application_id>')
@login_required
def admin_stipend_detail(application_id):
    """Admin view for individual stipend application details"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_stipend.dashboard'))
    
    # Convert application_id to int
    application_id = int(application_id)
    
    # Get application
    application = Application.query.get(application_id)
    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('admin_stipend.admin_stipend_applications'))
    
    # Get student and check if from admin's department
    student = User.query.filter_by(student_id=application.student_id).first()
    if not student or student.dept_id != current_user.dept_id:
        flash('Access denied. You can only view applications from your department.', 'danger')
        return redirect(url_for('admin_stipend.admin_stipend_applications'))
    
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


@admin_stipend_bp.route('/stipends/approve/<application_id>', methods=['POST'])
@login_required
def approve_stipend_application(application_id):
    """Approve a stipend application"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Convert application_id to int
    application_id = int(application_id)
    
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
    db.session.refresh(stipend)
    
    return jsonify({
        'success': True,
        'message': 'Application approved successfully'
    })


@admin_stipend_bp.route('/stipends/reject/<application_id>', methods=['POST'])
@login_required
def reject_stipend_application(application_id):
    """Reject a stipend application"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Convert application_id to int
    application_id = int(application_id)
    
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


@admin_stipend_bp.route('/stipends/view')
@login_required
def admin_view_stipends():
    """Admin view stipends page - displays all awarded stipends"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('admin_stipend.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get all awarded stipends for students in this department
    stipends = db.session.query(Stipend, User).join(
        User, Stipend.student_id == User.student_id
    ).filter(User.dept_id == current_user.dept_id).order_by(Stipend.awarded_at.desc()).all()
    
    return render_template('admin_stipends_view.html',
                         admin=current_user,
                         department=department,
                         stipends=stipends)


@admin_stipend_bp.route('/stipends/application-history')
@login_required
def application_history():
    """Admin view for all stipend application history (approved, rejected, pending)"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get filter from query params
    status_filter = request.args.get('status', 'all')
    
    # Get all applications for students in admin's department
    applications_query = db.session.query(Application).join(
        User, Application.student_id == User.student_id
    ).filter(User.dept_id == current_user.dept_id)
    
    # Apply status filter if not 'all'
    if status_filter != 'all':
        applications_query = applications_query.filter(Application.status == status_filter.capitalize())
    
    applications = applications_query.order_by(Application.created_at.desc()).all()
    
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
    
    return render_template('admin_stipend_history.html',
                         admin=current_user,
                         department=department,
                         applications=applications_data,
                         status_filter=status_filter)


