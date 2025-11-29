"""
Main Routes
Handles home and general dashboard routes
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import AcademicRecord, Admin

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Home page"""
    return render_template('home.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Unified dashboard - redirects based on user type"""
    # Check if user is admin or student
    if isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))
    else:
        # Student dashboard - show their info
        academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
        
        # Get current and last semester GPA
        current_gpa = academic_record.get_current_gpa() if academic_record else None
        last_semester_gpa = academic_record.get_last_semester_gpa() if academic_record else None
        last_completed_semester = academic_record.get_last_completed_semester() if academic_record else 0
        
        return render_template('dashboard.html',
                             user=current_user,
                             academic_record=academic_record,
                             current_gpa=current_gpa,
                             last_semester_gpa=last_semester_gpa,
                             last_completed_semester=last_completed_semester)


