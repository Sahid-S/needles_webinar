# Project Structure Guide

This document explains the organized structure of the Fashion Business Webinar Platform.

## Directory Overview

```
needles_webinar/
├── backend/              # Python Flask REST API
├── frontend/             # Static HTML/CSS/JS web application
├── deployment/           # Deployment configurations and guides
├── scripts/              # Utility scripts for development
└── README.md            # Main project documentation
```

## Backend (`/backend`)

Flask-based REST API handling OTP verification, payment processing, and webhooks.

### Structure
```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config/
│   │   └── config.py        # Environment configurations
│   ├── routes/
│   │   ├── otp.py          # OTP generation and verification
│   │   ├── validation.py   # Email/phone validation
│   │   └── payment.py      # Razorpay integration & webhooks
│   └── utils/
│       ├── email_service.py    # Amazon SES email sending
│       ├── payment_service.py  # Razorpay payment utilities
│       └── validators.py       # Input validation helpers
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

### Setup
1. Copy `.env.example` to `.env` and configure credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python run.py`

## Frontend (`/frontend`)

Static web application with multi-step registration, OTP verification, and payment integration.

### Structure
```
frontend/
├── index.html              # Landing page
├── register.html           # Main registration flow
├── css/
│   └── global.css          # Global styles and themes
├── js/
│   └── config.js           # API endpoint configuration
├── pages/
│   ├── contact.html        # Contact support page
│   ├── success.html        # Payment success page
│   ├── payment-failed.html # Payment failure page
│   ├── privacy-policy.html # Privacy policy
│   ├── refund-policy.html  # Refund policy
│   └── terms-conditions.html # Terms and conditions
└── images/                 # Image assets
```

### Setup
1. Update API endpoints in `js/config.js` or use the update script
2. Serve files with any static server (e.g., `python -m http.server 8000`)

## Deployment (`/deployment`)

Contains all deployment-related configurations and documentation.

### Files
- `DEPLOYMENT.md` - Comprehensive deployment guide for Render
- `Procfile` - Process configuration for Heroku/Render
- `render.yaml` - Render Blueprint configuration
- `runtime.txt` - Python version specification

### Usage
For Render deployment:
1. Push code to GitHub
2. Import repository in Render
3. Render will auto-detect `render.yaml`
4. Configure environment variables in Render dashboard

## Scripts (`/scripts`)

Utility scripts for development and deployment tasks.

### Available Scripts
- `update-api-urls.ps1` - Switch between development and production API endpoints

### Usage
```powershell
# Switch to development
.\scripts\update-api-urls.ps1 -Environment dev

# Switch to production
.\scripts\update-api-urls.ps1 -Environment prod
```

## Key Features

### Backend Features
- Email OTP generation and verification using Amazon SES
- Email and phone number validation
- Razorpay payment integration
- Secure webhook handling with signature verification
- CORS-enabled API endpoints
- Comprehensive error handling

### Frontend Features
- Multi-step registration form with validation
- Real-time OTP verification
- Integrated Razorpay payment gateway
- Responsive design for all devices
- Policy and information pages
- Payment success/failure handling

## Development Workflow

### Local Development
1. Start backend: `cd backend && python run.py`
2. Start frontend: `cd frontend && python -m http.server 8000`
3. Access application: `http://localhost:8000`

### Environment Configuration
- Backend uses `.env` file for configuration
- Frontend uses `js/config.js` for API endpoints
- Use `update-api-urls.ps1` script to quickly switch environments

### Before Deployment
1. Update production URLs in `js/config.js`
2. Ensure all environment variables are set in hosting platform
3. Test payment flow in Razorpay test mode
4. Verify email sending with Amazon SES

## Best Practices

### Code Organization
- Backend: Follow Flask blueprints pattern for routes
- Frontend: Separate concerns (HTML, CSS, JS in respective directories)
- Keep environment-specific configs in dedicated files

### Security
- Never commit `.env` files
- Use environment variables for all secrets
- Validate all user inputs on backend
- Verify webhook signatures

### Maintenance
- Backup files are automatically ignored (`.gitignore`)
- Update `requirements.txt` when adding Python packages
- Document API changes in backend README
- Update this guide when restructuring

## Additional Resources

- [Backend API Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)
- [Deployment Guide](deployment/DEPLOYMENT.md)
- [Main README](README.md)
