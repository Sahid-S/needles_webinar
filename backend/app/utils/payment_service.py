import hmac
import hashlib
import base64
import requests
from flask import current_app

def create_razorpay_order(amount, currency='INR', receipt=None, notes=None):
    """Create a Razorpay order"""
    config = current_app.config
    
    if receipt is None:
        from datetime import datetime
        receipt = f"webinar_{int(datetime.now().timestamp())}"
    
    if notes is None:
        notes = {}
    
    order_data = {
        'amount': amount,
        'currency': currency,
        'receipt': receipt,
        'notes': notes
    }
    
    auth_string = f"{config['RAZORPAY_KEY_ID']}:{config['RAZORPAY_KEY_SECRET']}"
    auth_bytes = auth_string.encode('utf-8')
    auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    response = requests.post(
        'https://api.razorpay.com/v1/orders',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_b64}'
        },
        json=order_data
    )
    
    order = response.json()
    
    if not response.ok:
        error_msg = order.get('error', {}).get('description', 'Failed to create order')
        raise Exception(error_msg)
    
    return order

def verify_razorpay_signature(order_id, payment_id, signature):
    """Verify Razorpay payment signature"""
    config = current_app.config
    
    body = f"{order_id}|{payment_id}"
    expected_signature = hmac.new(
        config['RAZORPAY_KEY_SECRET'].encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return expected_signature == signature

def verify_webhook_signature(webhook_body, received_signature):
    """Verify Razorpay webhook signature"""
    config = current_app.config
    
    expected_signature = hmac.new(
        config['RAZORPAY_WEBHOOK_SECRET'].encode('utf-8'),
        webhook_body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return received_signature == expected_signature
