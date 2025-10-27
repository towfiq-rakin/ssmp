"""
Authentication Routes
Handles login, logout, and user authentication
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Admin
from extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login for both students and admins"""
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email_or_id = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'student')  # Default to student
        remember = True if request.form.get('remember') else False
        
        user = None
        
        if user_type == 'admin':
            # Try to find admin by email
            user = Admin.query.filter_by(email=email_or_id).first()
        else:
            # Try to find student by email first
            user = User.query.filter_by(email=email_or_id).first()
            
            # If not found by email, try by student ID
            if not user:
                try:
                    student_id = int(email_or_id)
                    user = User.query.filter_by(student_id=student_id).first()
                except ValueError:
                    # Not a valid number, skip ID lookup
                    pass
        
        # Direct password comparison (plain text)
        # TODO: Implement password hashing for security
        if user and user.password == password:
            login_user(user, remember=remember)
            flash('Login successful!', 'success')
            
            # Redirect based on user type
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif isinstance(user, Admin):
                return redirect(url_for('main.admin_dashboard'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email/ID or password', 'danger')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
