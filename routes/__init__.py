"""
Routes Package
"""
from .auth import auth_bp
from .main import main_bp
from .admin import admin_bp
from .admin_scholarship import admin_scholarship_bp
from .admin_stipend import admin_stipend_bp
from .student import student_bp
from .student_actions import student_actions_bp

# Export all blueprints
__all__ = ['auth_bp', 'main_bp', 'admin_bp', 'admin_scholarship_bp', 'admin_stipend_bp', 'student_bp', 'student_actions_bp']
