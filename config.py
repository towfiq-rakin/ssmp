"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = 'your-secret-key-here'  # Change this to a random secret key in production
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ssmp_user:ssmp_password@localhost/ssmp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login settings
    LOGIN_VIEW = 'auth.login'
    LOGIN_MESSAGE = 'Please log in to access this page.'
    LOGIN_MESSAGE_CATEGORY = 'info'
    
    # Flask-Mail settings for Gmail SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('SSMP BUP', os.environ.get('MAIL_USERNAME'))
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
    
    # Email sending toggle - Set to False to disable all emails
    SEND_EMAILS = os.environ.get('SEND_EMAILS', 'True').lower() in ('true', '1', 'yes')


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
