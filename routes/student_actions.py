"""
Student Actions Routes
Handles student application submissions
"""
from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, Scholarship, Stipend, Application, IncomeRecord
from extensions import db
from datetime import datetime

student_actions_bp = Blueprint('student_actions', __name__)


@student_actions_bp.route('/stipends/apply', methods=['POST'])
@login_required
def apply_stipend():
    """Handle stipend application submission"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    # Check eligibility again based on LAST COMPLETED semester
    last_semester_gpa = academic_record.get_last_semester_gpa() if academic_record else None
    last_completed_semester = academic_record.get_last_completed_semester() if academic_record else 0
    
    if last_completed_semester <= 0:
        flash('You are not eligible for a stipend. No completed semester found.', 'danger')
        return redirect(url_for('student.stipends'))
    
    if not last_semester_gpa or last_semester_gpa < 3.5:
        flash('You are not eligible for a stipend. Minimum GPA required is 3.5', 'danger')
        return redirect(url_for('student.stipends'))
    
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
        flash('You have already received an award for this semester.', 'warning')
        return redirect(url_for('student.stipends'))
    
    # Check for pending application
    pending_application = Application.query.filter_by(
        student_id=current_user.student_id,
        status='Pending'
    ).first()
    
    if pending_application:
        flash('You already have a pending application.', 'warning')
        return redirect(url_for('student.stipends'))
    
    # Check for rejected application for the same semester
    rejected_application = Application.query.filter_by(
        student_id=current_user.student_id,
        semester=semester_name,
        status='Rejected'
    ).first()
    
    if rejected_application:
        flash('You cannot apply again for this semester as your previous application was rejected.', 'danger')
        return redirect(url_for('student.stipends'))
    
    # Get form data
    amount = request.form.get('amount')
    source = request.form.get('source')
    family_member = request.form.get('family_member')
    stipend_type = request.form.get('stipend_type')
    
    if not amount or not source or not family_member or not stipend_type:
        flash('Please fill in all fields.', 'danger')
        return redirect(url_for('student.stipends'))
    
    # Validate stipend type based on GPA
    if stipend_type == "Vice Chancellor Stipend" and last_semester_gpa < 3.75:
        flash('You are not eligible for Vice Chancellor Stipend. Minimum GPA required is 3.75', 'danger')
        return redirect(url_for('student.stipends'))
    
    if stipend_type not in ["BUP Stipend", "Vice Chancellor Stipend"]:
        flash('Invalid stipend type selected.', 'danger')
        return redirect(url_for('student.stipends'))
    
    try:
        amount = float(amount)
        family_member = int(family_member)
    except ValueError:
        flash('Invalid input values.', 'danger')
        return redirect(url_for('student.stipends'))
    
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
    
    flash('Your stipend application has been submitted successfully!', 'success')
    return redirect(url_for('student.stipends'))
