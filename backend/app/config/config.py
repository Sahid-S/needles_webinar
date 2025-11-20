import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PORT = int(os.getenv('PORT', 3000))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
    RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
    RAZORPAY_WEBHOOK_SECRET = os.getenv('RAZORPAY_WEBHOOK_SECRET')
    
    # Email Configuration (Amazon SES)
    SMTP_HOST = 'email-smtp.us-east-1.amazonaws.com'
    SMTP_PORT = 587
    SMTP_USERNAME = os.getenv('SMTP_USERNAME') or os.getenv('EMAIL_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD') or os.getenv('EMAIL_PASS')
    VERIFIED_SENDER = os.getenv('VERIFIED_SENDER', 'info@theneedles.in')
    
    # OTP Configuration
    OTP_EXPIRY_MINUTES = 10
    OTP_MAX_ATTEMPTS = 3
    
    # SQL Server Database Configuration
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'webinar_db')
    DB_USER = os.getenv('DB_USER', 'sa')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
