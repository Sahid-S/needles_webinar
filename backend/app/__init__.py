from flask import Flask
from flask_cors import CORS
from datetime import datetime

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    from app.config.config import config
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app)
    
    # Test database connection
    try:
        from app.database import test_connection
        if test_connection():
            print('✓ Database connection successful')
        else:
            print('⚠️  WARNING: Database connection failed!')
    except Exception as e:
        print(f'⚠️  WARNING: Database not configured: {e}')
    
    # Validate required configuration
    if not app.config['RAZORPAY_KEY_ID'] or not app.config['RAZORPAY_KEY_SECRET']:
        print('ERROR: Missing required Razorpay credentials in .env file')
        exit(1)
    
    if not app.config['SMTP_USERNAME'] or not app.config['SMTP_PASSWORD']:
        print('⚠️  WARNING: SMTP credentials not configured! OTP emails will not work.')
        print('⚠️  Add SMTP_USERNAME and SMTP_PASSWORD in environment variables.')
    else:
        print('✓ Email transporter initialized successfully')
        print(f"SMTP User: {app.config['SMTP_USERNAME']}")
        print(f"Verified Sender: {app.config['VERIFIED_SENDER']}")
        print('✓ Amazon SES configured (verification will happen on first email)')
    
    # Register blueprints
    from app.routes.otp import otp_bp
    from app.routes.validation import validation_bp
    from app.routes.payment import payment_bp
    
    app.register_blueprint(otp_bp)
    app.register_blueprint(validation_bp)
    app.register_blueprint(payment_bp)
    
    # Request logger middleware
    @app.before_request
    def log_request():
        from flask import request
        print(f"[{datetime.now().isoformat()}] {request.method} {request.path}")
    
    # Global error handler
    @app.errorhandler(Exception)
    def handle_error(error):
        from flask import request, jsonify
        print('=== GLOBAL ERROR HANDLER ===')
        print('Path:', request.path)
        print('Error:', str(error))
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(error)
        }), 500
    
    return app
