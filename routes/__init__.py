"""
Routes Package
"""
from .auth import auth_bp
from .main import main_bp

# Export all blueprints
__all__ = ['auth_bp', 'main_bp']
