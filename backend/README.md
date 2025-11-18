# Backend API

Flask-based REST API for webinar registration and payment processing.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config/
│   │   └── config.py         # Configuration settings
│   ├── routes/
│   │   ├── otp.py           # OTP endpoints
│   │   ├── validation.py    # Validation endpoints
│   │   └── payment.py       # Payment & webhook endpoints
│   └── utils/
│       ├── validators.py    # Input validation utilities
│       ├── email_service.py # Email/OTP service
│       └── payment_service.py # Razorpay integration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables

```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables in `.env`:**
   ```
   RAZORPAY_KEY_ID=your_key
   RAZORPAY_KEY_SECRET=your_secret
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   SMTP_USERNAME=your_smtp_user
   SMTP_PASSWORD=your_smtp_pass
   VERIFIED_SENDER=your@email.com
   PORT=3000
   ```

3. **Run the server:**
   ```bash
   python run.py
   ```

## API Endpoints

### OTP Management
- `POST /send-otp` - Send OTP to email
- `POST /verify-otp` - Verify OTP code

### Validation
- `POST /validate-contact` - Validate email and phone numbers

### Payment
- `POST /create-order` - Create Razorpay order
- `POST /verify-payment` - Verify payment signature
- `POST /webhook` - Handle Razorpay webhooks
- `GET /success` - Payment success page

## Features

- ✅ Email OTP verification (Amazon SES)
- ✅ Razorpay payment integration
- ✅ Webhook handling with signature verification
- ✅ Input validation (email, phone)
- ✅ Modular architecture with blueprints
- ✅ Configuration management
- ✅ Error handling and logging
