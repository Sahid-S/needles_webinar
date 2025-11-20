from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import os
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# In production, store this in database with hashed passwords
# For now, using environment variable
admin_password = os.getenv('ADMIN_PASSWORD_HASH', 'needles_admin_2025')
ADMIN_CREDENTIALS = {
    'admin': admin_password,
    'needles_admin': admin_password
}

ADMIN_SECRET_KEY = os.getenv('ADMIN_SECRET_KEY', 'needles_admin_secret_2025')

def verify_admin_token(f):
    """Decorator to verify admin token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('X-Admin-Token')
        if not token or token != ADMIN_SECRET_KEY:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Check if username exists
        if username not in ADMIN_CREDENTIALS:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Verify password
        stored_hash = ADMIN_CREDENTIALS[username]
        
        # For development, allow plain text comparison (REMOVE IN PRODUCTION)
        # In production, use only check_password_hash
        is_valid = False
        if stored_hash.startswith('pbkdf2:'):
            is_valid = check_password_hash(stored_hash, password)
        else:
            # Temporary plain text check for easy setup
            is_valid = (password == stored_hash)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Return success with token
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': ADMIN_SECRET_KEY,
            'username': username
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Login failed. Please try again.'
        }), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Verify admin token"""
    try:
        token = request.headers.get('X-Admin-Token')
        
        if not token or token != ADMIN_SECRET_KEY:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'Token is valid'
        }), 200
        
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Verification failed'
        }), 500
