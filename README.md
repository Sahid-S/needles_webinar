# Fashion Business Webinar Platform

A full-stack web application for webinar registration with email OTP verification and Razorpay payment integration.

## Project Structure

```
├── backend/                 # Flask REST API
│   ├── app/
│   │   ├── __init__.py     # Application factory
│   │   ├── config/         # Configuration settings
│   │   ├── routes/         # API endpoints
│   │   └── utils/          # Utilities & services
│   ├── run.py              # Entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/               # Static web application
│   ├── index.html         # Landing page
│   ├── register.html      # Registration form
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── pages/             # Additional pages
│   └── images/            # Image assets
│
├── deployment/            # Deployment configurations
│   ├── DEPLOYMENT.md      # Deployment guide
│   ├── Procfile           # Render/Heroku config
│   ├── render.yaml        # Render blueprint
│   └── runtime.txt        # Python version
│
├── scripts/               # Utility scripts
│   └── update-api-urls.ps1  # API URL updater
│
└── README.md             # This file
```

## Features

- ✅ Email OTP verification (Amazon SES)
- ✅ SQL Server database integration
- ✅ Contact validation (email & phone)
- ✅ Razorpay payment integration
- ✅ Webhook handling with signature verification
- ✅ Multi-step registration form
- ✅ Responsive design
- ✅ Payment success/failure handling

## Local Development

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup SQL Server Database:**
   - See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed instructions
   - Create database in SSMS
   - Configure connection in `.env`
   - Run: `python init_db.py` to create tables

5. Configure environment variables in `backend/.env`:
   ```env
   # Razorpay
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   
   # Email (Amazon SES)
   SMTP_USERNAME=your_smtp_username
   SMTP_PASSWORD=your_smtp_password
   VERIFIED_SENDER=your@email.com
   
   # Database
   DB_SERVER=localhost
   DB_NAME=webinar_db
   DB_USER=sa
   DB_PASSWORD=your_password
   
   PORT=3000
   ```

6. Run the server:
   ```bash
   python run.py
   ```

Backend will run on `http://localhost:3000`

### Frontend Setup

1. Open `frontend/index.html` in a browser

Or run a local server:
```bash
cd frontend
python -m http.server 8000
```

Visit `http://localhost:8000`

## Deployment to Render

### Backend Deployment (Web Service)

1. **Create a new Web Service** on Render

2. **Connect your repository**

3. **Configure the service:**
   - **Name:** `webinar-backend` (or your choice)
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Root Directory:** Leave empty (Procfile handles it)
   - **Environment:** `Python 3`
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && gunicorn run:app --bind 0.0.0.0:$PORT`

4. **Add Environment Variables:**
   Go to "Environment" tab and add:
   ```
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   SMTP_USERNAME=your_smtp_username
   SMTP_PASSWORD=your_smtp_password
   VERIFIED_SENDER=your@email.com
   FLASK_ENV=production
   PORT=10000
   ```

5. **Deploy:** Click "Create Web Service"

6. **Note your backend URL:** e.g., `https://webinar-backend.onrender.com`

### Frontend Deployment (Static Site)

1. **Create a new Static Site** on Render

2. **Connect your repository**

3. **Configure the site:**
   - **Name:** `webinar-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** Leave empty (static files)
   - **Publish Directory:** `.`

4. **Update API endpoints in `frontend/register.html`:**
   Replace `http://localhost:3000` with your Render backend URL:
   ```javascript
   const API_BASE = 'https://webinar-backend.onrender.com';
   ```

5. **Deploy:** Click "Create Static Site"

### Post-Deployment

1. **Update Razorpay Webhook URL:**
   - Go to Razorpay Dashboard → Webhooks
   - Add webhook URL: `https://your-backend.onrender.com/webhook`

2. **Test the application:**
   - Visit your frontend URL
   - Complete a test registration
   - Verify OTP email delivery
   - Test payment flow

## API Endpoints

- `POST /send-otp` - Send OTP to email
- `POST /verify-otp` - Verify OTP code
- `POST /validate-contact` - Validate email and phone
- `POST /create-order` - Create Razorpay order
- `POST /verify-payment` - Verify payment signature
- `POST /webhook` - Handle Razorpay webhooks
- `GET /success` - Payment success page

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `RAZORPAY_KEY_ID` | Razorpay API Key ID | Yes |
| `RAZORPAY_KEY_SECRET` | Razorpay API Secret | Yes |
| `RAZORPAY_WEBHOOK_SECRET` | Razorpay Webhook Secret | Yes |
| `SMTP_USERNAME` | Amazon SES SMTP Username | Yes |
| `SMTP_PASSWORD` | Amazon SES SMTP Password | Yes |
| `VERIFIED_SENDER` | Verified sender email | Yes |
| `PORT` | Server port (auto-set by Render) | No |
| `FLASK_ENV` | Environment (development/production) | No |

## Technologies Used

### Backend
- Python 3.12
- Flask (Web framework)
- Flask-CORS (Cross-origin resource sharing)
- Gunicorn (WSGI HTTP Server)
- Razorpay API
- Amazon SES (Email service)

### Frontend
- HTML5, CSS3, JavaScript
- Razorpay Checkout
- Responsive design

## Support

For issues or questions, please contact support.

## License

Private - All rights reserved
