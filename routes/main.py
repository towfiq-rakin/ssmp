"""
Main Routes
Handles home, dashboard, and other general routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from models import AcademicRecord, Admin, User, Department
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


@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard - displays students from admin's department"""
    # Check if user is admin
    if not isinstance(current_user, Admin):
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get search query
    search_query = request.args.get('search', '').strip()
    
    # Get department info
    department = current_user.get_department()
    
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
    
    return render_template('admin_dashboard.html',
                         admin=current_user,
                         department=department,
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
        return redirect(url_for('main.admin_dashboard'))
    
    # Check if student is from admin's department
    if student.dept_id != current_user.dept_id:
        flash('Access denied. You can only view students from your department.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    
    # Get student's department and academic record
    department = student.get_department()
    academic_record = AcademicRecord.query.filter_by(student_id=student.student_id).first()
    
    return render_template('admin_student_detail.html',
                         admin=current_user,
                         student=student,
                         department=department,
                         academic_record=academic_record)
