import json
from flask import Blueprint, request, jsonify
from app.utils.payment_service import (
    create_razorpay_order,
    verify_razorpay_signature,
    verify_webhook_signature
)

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create-order', methods=['POST'])
def create_order():
    """Create a Razorpay order"""
    try:
        data = request.json
        amount = data.get('amount', 100)  # ₹1 in paise
        currency = data.get('currency', 'INR')
        receipt = data.get('receipt')
        notes = data.get('notes', {})
        
        order = create_razorpay_order(amount, currency, receipt, notes)
        return jsonify(order)
    
    except Exception as error:
        print('Error creating order:', error)
        return jsonify({
            'error': str(error),
            'details': 'Failed to create Razorpay order'
        }), 500

@payment_bp.route('/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Razorpay payment signature"""
    try:
        data = request.json
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        is_valid = verify_razorpay_signature(
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        )
        
        if is_valid:
            print('Payment verified successfully:', {
                'order_id': razorpay_order_id,
                'payment_id': razorpay_payment_id
            })
            
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully',
                'order_id': razorpay_order_id,
                'payment_id': razorpay_payment_id
            })
        else:
            print('Payment verification failed')
            return jsonify({
                'success': False,
                'message': 'Payment verification failed'
            }), 400
    
    except Exception as error:
        print('Payment verification error:', error)
        return jsonify({
            'success': False,
            'message': 'Payment verification error',
            'error': str(error)
        }), 500

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Razorpay webhook events"""
    try:
        # Get the signature from headers
        received_signature = request.headers.get('X-Razorpay-Signature')
        
        # Get raw body
        webhook_body = request.get_data(as_text=True)
        
        # Verify signature
        is_valid = verify_webhook_signature(webhook_body, received_signature)
        
        if not is_valid:
            print('Webhook signature verification failed')
            return jsonify({'error': 'Invalid signature'}), 400
        
        # Parse the webhook payload
        webhook_data = json.loads(webhook_body)
        event = webhook_data.get('event')
        payload = webhook_data.get('payload')
        
        print('Webhook received:', event)
        print('Payload:', json.dumps(payload, indent=2))
        
        # Handle different webhook events
        if event == 'payment.authorized':
            print('Payment authorized:', payload['payment']['entity']['id'])
        elif event == 'payment.captured':
            print('Payment captured:', payload['payment']['entity']['id'])
            handle_successful_payment(payload['payment']['entity'])
        elif event == 'payment.failed':
            print('Payment failed:', payload['payment']['entity']['id'])
            handle_failed_payment(payload['payment']['entity'])
        elif event == 'order.paid':
            print('Order paid:', payload['order']['entity']['id'])
        else:
            print('Unhandled webhook event:', event)
        
        # Always respond with 200 to acknowledge receipt
        return jsonify({'received': True}), 200
    
    except Exception as error:
        print('Webhook error:', error)
        return jsonify({
            'error': 'Webhook processing failed',
            'message': str(error)
        }), 500

def handle_successful_payment(payment_entity):
    """Process successful payment"""
    print('Processing successful payment:', {
        'payment_id': payment_entity['id'],
        'order_id': payment_entity['order_id'],
        'amount': payment_entity['amount'] / 100,
        'email': payment_entity.get('email'),
        'contact': payment_entity.get('contact'),
        'method': payment_entity.get('method')
    })
    # Add your business logic here

def handle_failed_payment(payment_entity):
    """Process failed payment"""
    print('Processing failed payment:', {
        'payment_id': payment_entity['id'],
        'order_id': payment_entity['order_id'],
        'error_code': payment_entity.get('error_code'),
        'error_description': payment_entity.get('error_description')
    })
    # Add your business logic here

@payment_bp.route('/success', methods=['GET'])
def success_page():
    """Payment success page"""
    html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Payment Success - The Needles</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .success-container { max-width: 600px; margin: 0 auto; }
                .success-icon { font-size: 64px; color: #28a745; }
                h1 { color: #006478; }
                p { font-size: 18px; line-height: 1.6; }
                .btn { background: #006478; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="success-container">
                <div class="success-icon">✅</div>
                <h1>Payment Successful!</h1>
                <p>Thank you for registering for the Fashion Business Webinar!</p>
                <p>You will receive webinar details and Zoom link via email within 24 hours.</p>
                <p><strong>Webinar Date:</strong> 10th December 2025<br>
                <strong>Time:</strong> 9AM - 12PM (IST)</p>
                <a href="/" class="btn">Back to Home</a>
            </div>
        </body>
        </html>
    '''
    return html
