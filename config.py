"""
Application Configuration
"""

class Config:
    """Base configuration"""
    SECRET_KEY = 'your-secret-key-here'  # Change this to a random secret key in production
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ssmp_user:ssmp_password@localhost/ssmp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login settings
    LOGIN_VIEW = 'auth.login'
    LOGIN_MESSAGE = 'Please log in to access this page.'
    LOGIN_MESSAGE_CATEGORY = 'info'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
