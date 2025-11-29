"""
Admin Routes
Handles admin dashboard and student management
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, User, Department, Scholarship, Stipend
from extensions import db
from routes.analytics import get_admin_dashboard_data

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard - displays admin information and analytics"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get department info
    department = current_user.get_department()
    
    # Get analytics data
    analytics_data = get_admin_dashboard_data(current_user.dept_id, department.budget)

    return render_template('admin_dashboard.html',
                         admin=current_user,
                         department=department,
                         stats=analytics_data['stats'],
                         plots=analytics_data['plots'])


@admin_bp.route('/students')
@login_required
def students():
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
    
    # Execute query
    students = students_query.all()
    
    return render_template('admin_students.html',
                         admin=current_user,
                         students=students,
                         search_query=search_query)


@admin_bp.route('/student/<int:student_id>')
@login_required
def view_student(student_id):
    """View detailed information about a specific student"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get student
    student = User.query.get(student_id)
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('admin.students'))
    
    # Check if student belongs to admin's department
    if student.dept_id != current_user.dept_id:
        flash('Access denied. Student not in your department.', 'danger')
        return redirect(url_for('admin.students'))
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=student_id).first()
    
    return render_template('admin_student_detail.html',
                         admin=current_user,
                         student=student,
                         academic_record=academic_record)


@admin_bp.route('/student/<int:student_id>/academic-record/update', methods=['POST'])
@login_required
def update_academic_record(student_id):
    """Update student academic record"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get student
    student = User.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'}), 404
    
    # Check if student belongs to admin's department
    if student.dept_id != current_user.dept_id:
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    # Get academic record
    academic_record = AcademicRecord.query.filter_by(student_id=student_id).first()
    
    if not academic_record:
        return jsonify({'success': False, 'message': 'Academic record not found'}), 404
    
    # Get form data
    try:
        cgpa = float(request.form.get('cgpa', 0))
        current_semester = int(request.form.get('current_semester', 1))
        
        # Update CGPA and current semester
        academic_record.cgpa = cgpa
        academic_record.current_semester = current_semester
        
        # Update individual semester GPAs
        for i in range(1, 9):
            semester_gpa_key = f'semester_{i}_gpa'
            semester_gpa_value = request.form.get(semester_gpa_key)
            
            if semester_gpa_value and semester_gpa_value.strip():
                try:
                    gpa = float(semester_gpa_value)
                    setattr(academic_record, semester_gpa_key, gpa)
                except ValueError:
                    continue
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Academic record updated successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating academic record: {str(e)}'
        }), 400


@admin_bp.route('/scholarships/view')
@login_required
def view_scholarships():
    """Admin view scholarships page - displays all awarded scholarships"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
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


@admin_bp.route('/stipends/view')
@login_required
def view_stipends():
    """Admin view stipends page - displays all awarded stipends"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
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
