"""
Student Routes
Handles student-facing routes for scholarships and stipends
"""
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, Scholarship, Stipend, Application
from extensions import db

student_bp = Blueprint('student', __name__)


@student_bp.route('/scholarships')
@login_required
def scholarships():
    """Student scholarships page - displays eligibility and awarded scholarships"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=current_user.student_id).first()
    
    # Check eligibility based on LAST COMPLETED semester GPA
    is_eligible = False
    eligible_for_chancellor = False
    last_semester_gpa = None
    last_completed_semester = None
    ineligibility_reason = None
    
    if academic_record:
        last_semester_gpa = academic_record.get_last_semester_gpa()
        last_completed_semester = academic_record.get_last_completed_semester()
        
        # Scholarships are awarded based on the last completed semester GPA
        semester_name = f"Semester {last_completed_semester}" if last_completed_semester > 0 else None
        
        if not semester_name or last_completed_semester <= 0:
            ineligibility_reason = 'first_semester'
        else:
            # Check if already received scholarship for last completed semester
            existing_scholarship = Scholarship.query.filter_by(
                student_id=current_user.student_id,
                semester=semester_name
            ).first()
            
            # Check if already received stipend for last completed semester
            existing_stipend = Stipend.query.filter_by(
                student_id=current_user.student_id,
                semester=semester_name
            ).first()
            
            # Check eligibility and set reason if not eligible
            if existing_scholarship:
                ineligibility_reason = 'scholarship'
            elif existing_stipend:
                ineligibility_reason = 'stipend'
            elif last_semester_gpa and last_semester_gpa >= 3.8:
                is_eligible = True
                # Check if eligible for Chancellor Scholarship
                if last_semester_gpa >= 3.9:
                    eligible_for_chancellor = True
            else:
                ineligibility_reason = 'low_gpa_scholarship'
    
    # Get awarded scholarships
    scholarships = Scholarship.query.filter_by(student_id=current_user.student_id).order_by(Scholarship.awarded_at.desc()).all()
    
    return render_template('student_scholarships.html',
                         user=current_user,
                         academic_record=academic_record,
                         is_eligible=is_eligible,
                         eligible_for_chancellor=eligible_for_chancellor,
                         ineligibility_reason=ineligibility_reason,
                         scholarships=scholarships,
                         last_semester_gpa=last_semester_gpa,
                         last_completed_semester=last_completed_semester)


@student_bp.route('/stipends')
@login_required
def stipends():
    """Student stipends page - displays eligibility, application form and history"""
    # Check if user is admin
    if isinstance(current_user, Admin):
        return redirect(url_for('admin.dashboard'))
    
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
                is_eligible = False
            elif existing_stipend:
                ineligibility_reason = 'stipend'
                is_eligible = False
            elif last_semester_gpa and last_semester_gpa >= 3.5:
                is_eligible = True
                # Check if eligible for Vice Chancellor Stipend
                if last_semester_gpa >= 3.75:
                    eligible_for_vc = True
            else:
                ineligibility_reason = 'low_gpa'
                is_eligible = False
    
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
                         has_current_semester_scholarship=has_current_semester_scholarship,
                         has_current_semester_stipend=has_current_semester_stipend,
                         last_semester_gpa=last_semester_gpa,
                         last_completed_semester=last_completed_semester,
                         eligibility_criteria=eligibility_criteria)
