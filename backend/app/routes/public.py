"""
Public routes for fetching webinar information
"""
from flask import Blueprint, jsonify
from app.models import Settings
from datetime import datetime

public_bp = Blueprint('public', __name__)

@public_bp.route('/webinar-info', methods=['GET'])
def get_webinar_info():
    """
    Get webinar information (date, time, title)
    Public endpoint - no authentication required
    """
    try:
        info = Settings.get_webinar_info()
        # Don't expose zoom_link publicly
        return jsonify({
            'success': True,
            'webinar_date': info['webinar_date'],
            'webinar_time': info['webinar_time'],
            'webinar_title': info['webinar_title']
        })
    except Exception as error:
        print('Error fetching webinar info:', error)
        # Return defaults if table doesn't exist yet
        return jsonify({
            'success': True,
            'webinar_date': 'December 10, 2025',
            'webinar_time': '9:00 AM - 12:00 PM IST',
            'webinar_title': 'The Needles Webinar'
        })

@public_bp.route('/registration-status', methods=['GET'])
def get_registration_status():
    """
    Check if registrations are still open
    Returns registration status based on webinar date
    """
    try:
        info = Settings.get_webinar_info()
        webinar_date_str = info.get('webinar_date', 'December 10, 2025')
        
        # Parse webinar date
        try:
            # Try different date formats
            for fmt in ['%B %d, %Y', '%d %B %Y', '%d-%m-%Y', '%Y-%m-%d', '%d %B, %Y']:
                try:
                    webinar_date = datetime.strptime(webinar_date_str.strip(), fmt)
                    break
                except ValueError:
                    continue
            else:
                # If no format matches, default to allowing registration
                print(f'Could not parse date: {webinar_date_str}')
                return jsonify({
                    'success': True,
                    'registration_open': True,
                    'message': 'Registration is open'
                })
            
            # Check if webinar date has passed
            current_date = datetime.now()
            
            if current_date.date() >= webinar_date.date():
                return jsonify({
                    'success': True,
                    'registration_open': False,
                    'message': 'Registration is closed. The webinar has already started or ended.'
                })
            else:
                return jsonify({
                    'success': True,
                    'registration_open': True,
                    'message': 'Registration is open'
                })
                
        except Exception as date_error:
            print(f'Date parsing error: {date_error}')
            # Default to open if can't parse
            return jsonify({
                'success': True,
                'registration_open': True,
                'message': 'Registration is open'
            })
            
    except Exception as error:
        print('Error checking registration status:', error)
        # Default to open on error
        return jsonify({
            'success': True,
            'registration_open': True,
            'message': 'Registration is open'
        })
