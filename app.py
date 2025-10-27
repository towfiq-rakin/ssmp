"""
SSMP - Student Session Management Platform
Main Application Entry Point
"""
from flask import Flask
from config import config
from extensions import db, login_manager
from models import User


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
        return db.session.get(User, int(user_id))
    
    # Register blueprints
    from routes import auth_bp, main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app


# Create the app instance
app = create_app('development')


if __name__ == '__main__':
    app.run(debug=True)
