import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_email_otp(email, otp):
    """Send OTP via email using Amazon SES"""
    config = current_app.config
    
    msg = MIMEMultipart('alternative')
    msg['From'] = config['VERIFIED_SENDER']
    msg['To'] = email
    msg['Subject'] = 'Email Verification - The Needles Webinar'
    
    html_content = f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #006478;">Email Verification</h2>
            <p>Thank you for registering for the Fashion Business Webinar!</p>
            <p>Your verification code is:</p>
            <div style="background: #f5f5f5; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px;">
                <h1 style="color: #006478; font-size: 36px; letter-spacing: 5px; margin: 0;">{otp}</h1>
            </div>
            <p><strong>This code will expire in 10 minutes.</strong></p>
            <p>If you didn't request this code, please ignore this email.</p>
            <hr style="border: 1px solid #e9e9e9; margin: 30px 0;">
            <p style="color: #999; font-size: 12px; text-align: center;">
                The Needles - Fashion Business Webinar<br>
                December 10, 2025 | 9:00 AM - 12:00 PM IST
            </p>
        </div>
    '''
    
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT']) as server:
        server.starttls()
        server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
        server.send_message(msg)
