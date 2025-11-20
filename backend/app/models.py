"""
Database models for SQL Server operations
"""
from datetime import datetime, timedelta
from app.database import get_db_cursor

class Registration:
    """Registration model"""
    
    @staticmethod
    def create(data):
        """Create a new registration"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO registrations 
                (full_name, email, phone, whatsapp_number, city, state, 
                 business_name, business_type, experience_level, email_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('fullName'),
                data.get('email'),
                data.get('phone'),
                data.get('whatsappNumber'),
                data.get('city'),
                data.get('state'),
                data.get('businessName'),
                data.get('businessType'),
                data.get('experienceLevel'),
                1  # Email verified
            ))
            
            cursor.execute("SELECT @@IDENTITY")
            registration_id = cursor.fetchone()[0]
            return registration_id
    
    @staticmethod
    def get_by_email(email):
        """Get registration by email"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, full_name, email, phone, payment_status, 
                       razorpay_order_id, razorpay_payment_id
                FROM registrations 
                WHERE email = ?
            """, (email,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'payment_status': row[4],
                    'razorpay_order_id': row[5],
                    'razorpay_payment_id': row[6]
                }
            return None
    
    @staticmethod
    def update_payment(email, order_id, payment_id, status):
        """Update payment information"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE registrations 
                SET razorpay_order_id = ?,
                    razorpay_payment_id = ?,
                    payment_status = ?,
                    updated_at = GETDATE()
                WHERE email = ?
            """, (order_id, payment_id, status, email))
    
    @staticmethod
    def get_all():
        """Get all registrations"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, full_name, email, phone, city, state,
                       business_name, payment_status, created_at
                FROM registrations
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            registrations = []
            for row in rows:
                registrations.append({
                    'id': row[0],
                    'full_name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'city': row[4],
                    'state': row[5],
                    'business_name': row[6],
                    'payment_status': row[7],
                    'created_at': row[8]
                })
            return registrations


class OTP:
    """OTP verification model"""
    
    @staticmethod
    def create(email, otp, expiry_minutes=10):
        """Store OTP for email"""
        expiry = datetime.now() + timedelta(minutes=expiry_minutes)
        
        with get_db_cursor() as cursor:
            # Delete old OTPs for this email
            cursor.execute("DELETE FROM otp_verification WHERE email = ?", (email,))
            
            # Insert new OTP
            cursor.execute("""
                INSERT INTO otp_verification (email, otp, expiry, attempts)
                VALUES (?, ?, ?, 0)
            """, (email, otp, expiry))
    
    @staticmethod
    def get(email):
        """Get OTP record for email"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT otp, expiry, attempts
                FROM otp_verification
                WHERE email = ? AND expiry > GETDATE()
                ORDER BY created_at DESC
            """, (email,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'otp': row[0],
                    'expiry': row[1],
                    'attempts': row[2]
                }
            return None
    
    @staticmethod
    def increment_attempts(email):
        """Increment failed attempts"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE otp_verification
                SET attempts = attempts + 1
                WHERE email = ?
            """, (email,))
    
    @staticmethod
    def delete(email):
        """Delete OTP record"""
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM otp_verification WHERE email = ?", (email,))
    
    @staticmethod
    def cleanup_expired():
        """Remove expired OTPs"""
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM otp_verification WHERE expiry < GETDATE()")


class Payment:
    """Payment model"""
    
    @staticmethod
    def create(registration_id, order_id, amount):
        """Create payment record"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO payments 
                (registration_id, razorpay_order_id, amount, status)
                VALUES (?, ?, ?, 'pending')
            """, (registration_id, order_id, amount))
    
    @staticmethod
    def update(order_id, payment_id, signature, status, method=None):
        """Update payment status"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE payments
                SET razorpay_payment_id = ?,
                    razorpay_signature = ?,
                    status = ?,
                    payment_method = ?
                WHERE razorpay_order_id = ?
            """, (payment_id, signature, status, method, order_id))
    
    @staticmethod
    def get_by_order_id(order_id):
        """Get payment by order ID"""
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT id, registration_id, amount, status
                FROM payments
                WHERE razorpay_order_id = ?
            """, (order_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'registration_id': row[1],
                    'amount': row[2],
                    'status': row[3]
                }
            return None


class Settings:
    """Settings model for webinar configuration"""
    
    @staticmethod
    def get_setting(key):
        """Get a setting value by key"""
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT value FROM settings WHERE setting_key = ?",
                (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else None
    
    @staticmethod
    def set_setting(key, value):
        """Set or update a setting value"""
        with get_db_cursor() as cursor:
            # Check if setting exists
            cursor.execute(
                "SELECT id FROM settings WHERE setting_key = ?",
                (key,)
            )
            exists = cursor.fetchone()
            
            if exists:
                # Update existing
                cursor.execute(
                    "UPDATE settings SET value = ?, updated_at = GETDATE() WHERE setting_key = ?",
                    (value, key)
                )
            else:
                # Insert new
                cursor.execute(
                    "INSERT INTO settings (setting_key, value) VALUES (?, ?)",
                    (key, value)
                )
            
            return True
    
    @staticmethod
    def get_all_settings():
        """Get all settings as a dictionary"""
        with get_db_cursor() as cursor:
            cursor.execute("SELECT setting_key, value FROM settings")
            rows = cursor.fetchall()
            return {row[0]: row[1] for row in rows}
    
    @staticmethod
    def get_webinar_info():
        """Get webinar date and time information"""
        settings = Settings.get_all_settings()
        return {
            'webinar_date': settings.get('webinar_date', 'December 10, 2025'),
            'webinar_time': settings.get('webinar_time', '9:00 AM - 12:00 PM IST'),
            'webinar_title': settings.get('webinar_title', 'The Needles Webinar'),
            'zoom_link': settings.get('zoom_link', '')
        }
    
    @staticmethod
    def update_webinar_info(date=None, time=None, title=None, zoom_link=None):
        """Update webinar information"""
        if date:
            Settings.set_setting('webinar_date', date)
        if time:
            Settings.set_setting('webinar_time', time)
        if title:
            Settings.set_setting('webinar_title', title)
        if zoom_link:
            Settings.set_setting('zoom_link', zoom_link)
        return True
