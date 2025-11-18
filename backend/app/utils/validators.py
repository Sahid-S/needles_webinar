import re

def validate_email(email):
    """Validate email address format"""
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

def validate_phone(phone):
    """Validate Indian phone number format"""
    # Remove all non-digit characters
    clean_phone = re.sub(r'\D', '', phone)
    # Indian phone numbers: 10 digits (without country code) or 12 digits (with +91)
    return len(clean_phone) == 10 or (len(clean_phone) == 12 and clean_phone.startswith('91'))
