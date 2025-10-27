"""
SSMP - Student Session Management Platform
Main Application Entry Point
"""
from flask import Flask
from config import config
from extensions import db, login_manager
from models import User, Admin


def create_app(config_name='development'):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('admin_'):
            admin_id = int(user_id.replace('admin_', ''))
            return db.session.get(Admin, admin_id)
        elif user_id.startswith('student_'):
            student_id = int(user_id.replace('student_', ''))
            return db.session.get(User, student_id)
        return None
    
    # Register blueprints
    from routes import auth_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app


# Create the app instance
app = create_app('development')


if __name__ == '__main__':
    app.run(debug=True)
