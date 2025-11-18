from flask import Blueprint, request, jsonify
from app.utils.validators import validate_email, validate_phone

validation_bp = Blueprint('validation', __name__)

@validation_bp.route('/validate-contact', methods=['POST'])
def validate_contact():
    """Validate email and phone numbers"""
    try:
        data = request.json
        email = data.get('email')
        phone = data.get('phone')
        whatsapp = data.get('whatsapp')
        errors = {}
        
        # Validate email
        if not email or not validate_email(email):
            errors['email'] = 'Please enter a valid email address'
        
        # Validate phone
        if not phone or not validate_phone(phone):
            errors['phone'] = 'Please enter a valid 10-digit phone number'
        
        # Validate WhatsApp
        if not whatsapp or not validate_phone(whatsapp):
            errors['whatsapp'] = 'Please enter a valid 10-digit WhatsApp number'
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Contact details validated successfully'
        })
    
    except Exception as error:
        print('Validation error:', error)
        return jsonify({
            'success': False,
            'message': 'Validation failed',
            'error': str(error)
        }), 500
