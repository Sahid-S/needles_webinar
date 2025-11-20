"""
Admin routes for managing registrations and sending bulk emails
"""
from flask import Blueprint, request, jsonify
from app.models import Registration, Settings
from app.utils.email_service import send_webinar_link_email
from app.routes.auth import verify_admin_token
import time

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/send-webinar-links', methods=['POST'])
@verify_admin_token
def send_webinar_links():
    """
    Send webinar Zoom link to all registered participants
    Requires X-Admin-Token header for authentication
    
    Request body:
    {
        "zoom_link": "https://zoom.us/j/xxxxx",
        "webinar_date": "December 10, 2025",  # Optional
        "webinar_time": "9:00 AM - 12:00 PM IST"  # Optional
    }
    """
    try:
        data = request.json
        zoom_link = data.get('zoom_link')
        webinar_date = data.get('webinar_date', 'December 10, 2025')
        webinar_time = data.get('webinar_time', '9:00 AM - 12:00 PM IST')
        
        if not zoom_link:
            return jsonify({
                'success': False,
                'message': 'Zoom link is required'
            }), 400
        
        # Get all registrations with successful payment
        all_registrations = Registration.get_all()
        
        # Filter only those with successful payment
        paid_registrations = [r for r in all_registrations if r['payment_status'] == 'success']
        
        if not paid_registrations:
            return jsonify({
                'success': False,
                'message': 'No paid registrations found'
            }), 404
        
        print(f'Sending webinar links to {len(paid_registrations)} participants...')
        
        success_count = 0
        failed_count = 0
        failed_emails = []
        
        for registration in paid_registrations:
            try:
                email = registration['email']
                name = registration['full_name']
                
                send_webinar_link_email(email, name, zoom_link, webinar_date, webinar_time)
                success_count += 1
                print(f'✓ Sent to: {email}')
                
                # Add small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                failed_count += 1
                failed_emails.append({
                    'email': registration['email'],
                    'error': str(e)
                })
                print(f'✗ Failed to send to {registration["email"]}: {e}')
        
        return jsonify({
            'success': True,
            'message': f'Webinar links sent successfully',
            'total': len(paid_registrations),
            'sent': success_count,
            'failed': failed_count,
            'failed_emails': failed_emails if failed_emails else None
        })
    
    except Exception as error:
        print('Error sending webinar links:', error)
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'Failed to send webinar links',
            'error': str(error)
        }), 500

@admin_bp.route('/registrations', methods=['GET'])
@verify_admin_token
def get_registrations():
    """
    Get all registrations with their payment status
    Requires X-Admin-Token header for authentication
    """
    try:
        registrations = Registration.get_all()
        
        return jsonify({
            'success': True,
            'total': len(registrations),
            'registrations': registrations
        })
    
    except Exception as error:
        print('Error fetching registrations:', error)
        return jsonify({
            'success': False,
            'message': 'Failed to fetch registrations',
            'error': str(error)
        }), 500

@admin_bp.route('/webinar-settings', methods=['GET', 'POST'])
@verify_admin_token
def manage_webinar_settings():
    """
    Get or update webinar settings (date, time, title, zoom link)
    Requires X-Admin-Token header for authentication
    """
    try:
        if request.method == 'GET':
            # Get current settings
            settings = Settings.get_webinar_info()
            return jsonify({
                'success': True,
                'settings': settings
            })
        
        elif request.method == 'POST':
            # Update settings
            data = request.json
            
            Settings.update_webinar_info(
                date=data.get('webinar_date'),
                time=data.get('webinar_time'),
                title=data.get('webinar_title'),
                zoom_link=data.get('zoom_link')
            )
            
            return jsonify({
                'success': True,
                'message': 'Webinar settings updated successfully',
                'settings': Settings.get_webinar_info()
            })
    
    except Exception as error:
        print('Error managing webinar settings:', error)
        return jsonify({
            'success': False,
            'message': 'Failed to manage webinar settings',
            'error': str(error)
        }), 500
