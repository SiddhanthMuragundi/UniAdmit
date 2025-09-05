import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
    DB_NAME = os.environ.get('DB_NAME', 'student_admission_db')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Security configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'your-password-salt-here'
    
    # Use Argon2 for password hashing
    SECURITY_PASSWORD_HASH = 'argon2'
    
    # Token-based authentication
    SECURITY_TRACKABLE = True
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'Authentication-Token'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = 86400  # 24 hours
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size (allows for form data + 2 files)
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
    
    # Disable some Flask-Security features we don't need
    SECURITY_REGISTERABLE = False  # We'll handle registration ourselves
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_CHANGEABLE = False
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Default Admin Configuration
    ADMIN_NAME = os.environ.get('ADMIN_NAME', 'Admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@email.com')
    ADMIN_PHONE = os.environ.get('ADMIN_PHONE', '1234567890')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'adminpassword')
    ADMIN_ADDRESS = os.environ.get('ADMIN_ADDRESS', 'Admin HQ')
    ADMIN_COUNTRY = os.environ.get('ADMIN_COUNTRY', 'India')
    ADMIN_STATE = os.environ.get('ADMIN_STATE', 'Karnataka')
    ADMIN_DISTRICT = os.environ.get('ADMIN_DISTRICT', 'Bengaluru')
    ADMIN_PINCODE = os.environ.get('ADMIN_PINCODE', '560001')
    
    # Mail configuration (optional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
