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
    msg['From'] = f"The Needles Webinar <{config['VERIFIED_SENDER']}>"
    msg['To'] = email
    msg['Subject'] = f'Your verification code is {otp}'
    msg['Reply-To'] = config['VERIFIED_SENDER']
    msg['X-Priority'] = '1'  # High priority
    msg['Importance'] = 'high'
    msg['X-Entity-Ref-ID'] = 'account-verification'
    
    # Plain text version (important for spam filters)
    text_content = f'''
Your Verification Code: {otp}

Thank you for registering for The Needles Fashion Business Webinar.

Enter this code to verify your email address. This code expires in 10 minutes.

If you did not request this code, please ignore this email.

---
The Needles - Fashion Business Webinar
December 10, 2025 | 9:00 AM - 12:00 PM IST
    '''
    
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="padding: 40px 30px; text-align: center; background-color: #006478;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Email Verification Required</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 30px;">
                            <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                                Thank you for registering for The Needles Fashion Business Webinar.
                            </p>
                            <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px;">
                                Your verification code is:
                            </p>
                            <table width="100%" cellpadding="20" cellspacing="0">
                                <tr>
                                    <td align="center" style="background-color: #f8f9fa; border: 2px solid #006478; border-radius: 8px;">
                                        <span style="font-size: 32px; font-weight: bold; color: #006478; letter-spacing: 8px; font-family: monospace;">{otp}</span>
                                    </td>
                                </tr>
                            </table>
                            <p style="color: #d9534f; font-size: 14px; font-weight: bold; margin: 20px 0; text-align: center;">
                                This code expires in 10 minutes
                            </p>
                            <p style="color: #666; font-size: 14px; line-height: 1.6; margin: 20px 0 0;">
                                If you did not request this verification code, you can safely ignore this email.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px 30px; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                            <p style="color: #6c757d; font-size: 12px; margin: 0; text-align: center; line-height: 1.5;">
                                The Needles - Fashion Business Webinar<br>
                                December 10, 2025 | 9:00 AM - 12:00 PM IST
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    '''
    
    # Attach both plain text and HTML (improves deliverability)
    msg.attach(MIMEText(text_content, 'plain'))
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT']) as server:
        server.starttls()
        server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
        server.send_message(msg)

def send_confirmation_email(email, name, payment_id, order_id, webinar_date='December 10, 2025', webinar_time='9:00 AM - 12:00 PM IST'):
    """Send confirmation email after successful payment"""
    config = current_app.config
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"The Needles Webinar <{config['VERIFIED_SENDER']}>"
    msg['To'] = email
    msg['Subject'] = 'Your Webinar Registration is Confirmed - The Needles'
    msg['Reply-To'] = config['VERIFIED_SENDER']
    msg['List-Unsubscribe'] = f'<mailto:{config["VERIFIED_SENDER"]}?subject=unsubscribe>'
    
    html_content = f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
            <div style="background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #006478; margin: 0;">✅ Registration Confirmed!</h1>
                </div>
                
                <p style="font-size: 16px; color: #333;">Dear {name},</p>
                
                <p style="font-size: 16px; color: #333; line-height: 1.6;">
                    Thank you for registering for the <strong>Fashion Business Webinar</strong>! 
                    We're excited to have you join us.
                </p>
                
                <div style="background: linear-gradient(135deg, #006478 0%, #fee901 100%); padding: 25px; border-radius: 10px; margin: 30px 0;">
                    <h2 style="color: white; margin: 0 0 15px 0; font-size: 20px;">📅 Webinar Details</h2>
                    <p style="color: white; margin: 5px 0; font-size: 16px;"><strong>Date:</strong> {webinar_date}</p>
                    <p style="color: white; margin: 5px 0; font-size: 16px;"><strong>Time:</strong> {webinar_time}</p>
                    <p style="color: white; margin: 5px 0; font-size: 16px;"><strong>Duration:</strong> 3 Hours</p>
                    <p style="color: white; margin: 5px 0; font-size: 16px;"><strong>Mode:</strong> Online (Zoom)</p>
                </div>
                
                <div style="background-color: #f0f8f9; padding: 20px; border-radius: 8px; border-left: 4px solid #006478; margin: 25px 0;">
                    <h3 style="color: #006478; margin: 0 0 10px 0; font-size: 16px;">Payment Details</h3>
                    <p style="margin: 5px 0; color: #555; font-size: 14px;"><strong>Payment ID:</strong> {payment_id}</p>
                    <p style="margin: 5px 0; color: #555; font-size: 14px;"><strong>Order ID:</strong> {order_id}</p>
                    <p style="margin: 5px 0; color: #28a745; font-size: 14px;"><strong>Status:</strong> ✅ Paid</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #006478; font-size: 18px;">What's Next?</h3>
                    <ul style="color: #555; line-height: 1.8; font-size: 15px;">
                        <li>You will receive the <strong>Zoom link</strong> 24 hours before the webinar</li>
                        <li>Check your email for <strong>pre-webinar materials</strong> and agenda</li>
                        <li>Mark your calendar and set a reminder</li>
                        <li>Prepare your questions for the live Q&A session</li>
                    </ul>
                </div>
                
                <div style="background-color: #fff9e6; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: #ff6b00; margin: 0 0 10px 0; font-size: 16px;">📚 What You'll Learn</h3>
                    <ul style="color: #555; line-height: 1.8; font-size: 14px; margin: 10px 0;">
                        <li>Building a successful fashion business from scratch</li>
                        <li>Marketing strategies for fashion entrepreneurs</li>
                        <li>Managing finances and scaling your business</li>
                        <li>Industry insights from experienced professionals</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p style="color: #666; font-size: 14px; margin-bottom: 10px;">Need help? Contact us:</p>
                    <p style="color: #006478; font-size: 14px; margin: 5px 0;">📧 Email: support@theneedles.com</p>
                    <p style="color: #006478; font-size: 14px; margin: 5px 0;">📱 WhatsApp: +91 XXXXX XXXXX</p>
                </div>
                
                <hr style="border: 1px solid #e9e9e9; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px; text-align: center; line-height: 1.6;">
                    This is an automated confirmation email. Please do not reply to this email.<br>
                    © 2025 The Needles. All rights reserved.
                </p>
            </div>
        </div>
    '''
    
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT']) as server:
        server.starttls()
        server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
        server.send_message(msg)

def send_webinar_link_email(email, name, zoom_link, webinar_date='December 10, 2025', webinar_time='9:00 AM - 12:00 PM IST'):
    """Send webinar Zoom link to registered participants"""
    config = current_app.config
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"The Needles Webinar <{config['VERIFIED_SENDER']}>"
    msg['To'] = email
    msg['Subject'] = 'Your Webinar Zoom Link - The Needles Fashion Business Event'
    msg['Reply-To'] = config['VERIFIED_SENDER']
    msg['List-Unsubscribe'] = f'<mailto:{config["VERIFIED_SENDER"]}?subject=unsubscribe>'
    
    html_content = f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
            <div style="background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #006478; margin: 0;">🎉 Get Ready for the Webinar!</h1>
                </div>
                
                <p style="font-size: 16px; color: #333;">Dear {name},</p>
                
                <p style="font-size: 16px; color: #333; line-height: 1.6;">
                    We're excited to see you at the <strong>Fashion Business Webinar</strong>! 
                    Here's everything you need to join us.
                </p>
                
                <div style="background: linear-gradient(135deg, #006478 0%, #fee901 100%); padding: 30px; border-radius: 10px; margin: 30px 0; text-align: center;">
                    <h2 style="color: white; margin: 0 0 20px 0; font-size: 20px;">📅 Webinar Details</h2>
                    <p style="color: white; margin: 5px 0; font-size: 16px;"><strong>Date:</strong> {webinar_date}</p>
                    <p style="color: white; margin: 5px 0; font-size: 16px;"><strong>Time:</strong> {webinar_time}</p>
                    <p style="color: white; margin: 5px 0 20px 0; font-size: 16px;"><strong>Duration:</strong> 3 Hours</p>
                    
                    <a href="{zoom_link}" style="display: inline-block; background-color: white; color: #006478; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 18px; margin-top: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                        🎥 Join Zoom Webinar
                    </a>
                </div>
                
                <div style="background-color: #fff9e6; padding: 20px; border-radius: 8px; border-left: 4px solid #ff6b00; margin: 25px 0;">
                    <h3 style="color: #ff6b00; margin: 0 0 10px 0; font-size: 16px;">⚠️ Important Instructions</h3>
                    <ul style="color: #555; line-height: 1.8; font-size: 14px; margin: 10px 0; padding-left: 20px;">
                        <li>Join <strong>5-10 minutes early</strong> to test your audio/video</li>
                        <li>Use a <strong>stable internet connection</strong></li>
                        <li>Keep your <strong>microphone muted</strong> unless speaking</li>
                        <li>Use the <strong>chat feature</strong> for questions during Q&A</li>
                        <li>Have a <strong>notebook ready</strong> to take notes</li>
                    </ul>
                </div>
                
                <div style="background-color: #f0f8f9; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: #006478; margin: 0 0 15px 0; font-size: 16px;">🔗 Zoom Meeting Details</h3>
                    <p style="margin: 8px 0; color: #555; font-size: 14px;"><strong>Zoom Link:</strong></p>
                    <p style="margin: 5px 0; word-break: break-all;">
                        <a href="{zoom_link}" style="color: #006478; text-decoration: underline;">{zoom_link}</a>
                    </p>
                    <p style="margin-top: 15px; color: #888; font-size: 12px;">
                        💡 <em>Tip: Click the link above or copy-paste it into your browser</em>
                    </p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #006478; font-size: 18px;">📚 What You'll Learn Today</h3>
                    <ul style="color: #555; line-height: 1.8; font-size: 15px;">
                        <li>Building a successful fashion business from scratch</li>
                        <li>Marketing strategies for fashion entrepreneurs</li>
                        <li>Managing finances and scaling your business</li>
                        <li>Industry insights from experienced professionals</li>
                        <li>Live Q&A with industry experts</li>
                    </ul>
                </div>
                
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                    <p style="color: #2e7d32; margin: 0; font-size: 15px; font-weight: 500;">
                        🎁 All participants will receive a <strong>Certificate of Participation</strong> 
                        and lifetime access to the webinar recording!
                    </p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p style="color: #666; font-size: 14px; margin-bottom: 10px;">Having trouble joining? Contact us:</p>
                    <p style="color: #006478; font-size: 14px; margin: 5px 0;">📧 Email: support@theneedles.com</p>
                    <p style="color: #006478; font-size: 14px; margin: 5px 0;">📱 WhatsApp: +91 XXXXX XXXXX</p>
                </div>
                
                <hr style="border: 1px solid #e9e9e9; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px; text-align: center; line-height: 1.6;">
                    We can't wait to see you there! 🎉<br>
                    © 2025 The Needles. All rights reserved.
                </p>
            </div>
        </div>
    '''
    
    msg.attach(MIMEText(html_content, 'html'))
    
    with smtplib.SMTP(config['SMTP_HOST'], config['SMTP_PORT']) as server:
        server.starttls()
        server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
        server.send_message(msg)
