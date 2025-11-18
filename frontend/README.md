# Frontend

Web application for webinar registration with OTP verification and payment integration.

## Structure

```
frontend/
├── index.html          # Landing page
├── register.html       # Registration form with OTP verification and payment
├── css/
│   └── global.css      # Global styles
├── js/
│   └── config.js       # API configuration (switch between dev/prod)
├── pages/
│   ├── success.html           # Payment success page
│   ├── payment-failed.html    # Payment failure page
│   ├── contact.html           # Contact page
│   ├── privacy-policy.html    # Privacy policy
│   ├── refund-policy.html     # Refund policy
│   └── terms-conditions.html  # Terms and conditions
└── images/             # Image assets
```

## Setup

1. **Update API endpoints:**
   - The registration form uses `http://localhost:3000` (local backend)
   - To switch environments, run the script: `../scripts/update-api-urls.ps1 -Environment dev` or `prod`
   - Or manually update endpoints in `js/config.js`

2. **Run locally:**
   - Simply open `index.html` in a browser
   - Or use a local server:
     ```bash
     python -m http.server 8000
     ```
   - Then visit `http://localhost:8000`

3. **Ensure backend is running:**
   - Backend must be running on `http://localhost:3000`
   - See `../backend/README.md` for backend setup

## Features

- ✅ Multi-step registration form
- ✅ Email OTP verification
- ✅ Contact validation (email, phone)
- ✅ Razorpay payment integration
- ✅ Payment success/failure handling
- ✅ Responsive design
- ✅ Form validation

## API Integration

The frontend connects to these backend endpoints:

- `POST /send-otp` - Send OTP to email
- `POST /verify-otp` - Verify OTP
- `POST /validate-contact` - Validate contact details
- `POST /create-order` - Create Razorpay order
- `POST /verify-payment` - Verify payment
- `GET /success` - Success page

## Configuration

Edit API endpoints in `register.html` or create a centralized config:

```javascript
// Current: Local development
const API_BASE = 'http://localhost:3000';

// Production
const API_BASE = 'https://your-production-api.com';
```
