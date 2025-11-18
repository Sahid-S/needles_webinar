from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from app.utils.validators import validate_email
from app.utils.email_service import generate_otp, send_email_otp
from app.models import OTP

otp_bp = Blueprint('otp', __name__)

@otp_bp.route('/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to user's email"""
    print('=== SEND OTP ENDPOINT CALLED ===')
    print('Request body:', request.json)
    print('Timestamp:', datetime.now().isoformat())
    
    try:
        data = request.json
        email = data.get('email')
        
        if not validate_email(email):
            print(f'Invalid email format: {email}')
            return jsonify({
                'success': False,
                'message': 'Invalid email address'
            }), 400
        
        otp = generate_otp()
        print(f'Generated OTP for {email}: {otp}')
        
        # Store OTP in database
        config = current_app.config
        OTP.create(email, otp, config['OTP_EXPIRY_MINUTES'])
        
        print('Attempting to send email...')
        send_email_otp(email, otp)
        print('Email sent successfully')
        
        print(f'Email OTP sent to {email}: {otp}')  # For development/testing
        
        return jsonify({
            'success': True,
            'message': 'OTP sent to your email'
        })
    
    except Exception as error:
        print('=== SEND OTP ERROR ===')
        print('Error message:', str(error))
        print('Error type:', type(error).__name__)
        
        if 'authentication' in str(error).lower() or 'auth' in str(error).lower():
            return jsonify({
                'success': False,
                'message': 'Email service not configured. Please contact support.',
                'error': 'SMTP credentials missing or invalid'
            }), 500
        
        return jsonify({
            'success': False,
            'message': 'Failed to send OTP. Please try again or contact support.',
            'error': str(error)
        }), 500

@otp_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify the OTP entered by user"""
    try:
        data = request.json
        email = data.get('email')
        otp = data.get('otp')
        config = current_app.config
        
        # Get OTP from database
        stored = OTP.get(email)
        
        if not stored:
            return jsonify({
                'success': False,
                'message': 'OTP not found or expired. Please request a new one.'
            }), 400
        
        # Check attempts
        if stored['attempts'] >= config['OTP_MAX_ATTEMPTS']:
            OTP.delete(email)
            return jsonify({
                'success': False,
                'message': 'Too many failed attempts. Please request a new OTP.'
            }), 400
        
        # Verify OTP
        if stored['otp'] == otp:
            OTP.delete(email)
            return jsonify({
                'success': True,
                'message': 'Email verified successfully'
            })
        else:
            OTP.increment_attempts(email)
            remaining = config['OTP_MAX_ATTEMPTS'] - (stored['attempts'] + 1)
            return jsonify({
                'success': False,
                'message': f"Invalid OTP. {remaining} attempts remaining."
            }), 400
    
    except Exception as error:
        print('Verify OTP error:', error)
        return jsonify({
            'success': False,
            'message': 'OTP verification failed',
            'error': str(error)
        }), 500
