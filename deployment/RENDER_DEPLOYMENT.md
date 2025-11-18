# Deploy Backend to Render - Complete Guide

## 🚀 Prerequisites

- GitHub account with your code pushed
- Render account (free tier available): https://render.com
- SQL Server database (your existing: 18.204.144.126)
- Razorpay API credentials
- Amazon SES SMTP credentials

## 📋 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Ensure all changes are committed:**
```powershell
git add .
git commit -m "Add database integration and production configs"
git push origin main
```

2. **Verify these files exist:**
- `backend/requirements-prod.txt` ✅
- `deployment/render.yaml` ✅
- `deployment/Procfile` ✅

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Deploy Backend API

#### Option A: Using Blueprint (Recommended)

1. **In Render Dashboard:**
   - Click **"New"** → **"Blueprint"**
   - Connect your GitHub repository: `needles_webinar`
   - Render will detect `deployment/render.yaml`
   - Click **"Apply"**

2. **Configure Environment Variables:**
   
   Go to your backend service → **Environment** tab and add:

   ```env
   # Flask
   FLASK_ENV=production
   PORT=10000
   
   # Razorpay
   RAZORPAY_KEY_ID=your_live_key_id
   RAZORPAY_KEY_SECRET=your_live_secret
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   
   # Email (Amazon SES)
   SMTP_USERNAME=your_smtp_username
   SMTP_PASSWORD=your_smtp_password
   VERIFIED_SENDER=jamindustries.info@gmail.com
   
   # Database (SQL Server)
   DB_DRIVER=ODBC Driver 17 for SQL Server
   DB_SERVER=18.204.144.126
   DB_NAME=webinar_db
   DB_USER=Appuser
   DB_PASSWORD=your_database_password
   ```

3. **Save and Deploy**
   - Click **"Save Changes"**
   - Render will automatically redeploy

#### Option B: Manual Web Service Creation

1. **Create Web Service:**
   - Dashboard → **"New"** → **"Web Service"**
   - Connect repository: `needles_webinar`
   - Configure:
     - **Name:** `webinar-backend`
     - **Region:** Choose closest to your users
     - **Branch:** `main`
     - **Root Directory:** Leave empty
     - **Environment:** `Python 3`
     - **Build Command:** `pip install -r backend/requirements-prod.txt`
     - **Start Command:** `cd backend && gunicorn run:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2`

2. **Add Environment Variables** (same as Option A above)

3. **Click "Create Web Service"**

### Step 4: Initialize Database Tables

**Important:** Run this ONCE after first deployment

1. **Use Render Shell:**
   - Go to your service → **"Shell"** tab
   - Run:
   ```bash
   cd backend
   python init_db.py
   ```

2. **Or run locally against remote DB:**
   ```powershell
   # Update your local .env with production DB credentials
   cd backend
   python init_db.py
   ```

### Step 5: Verify Deployment

1. **Check Logs:**
   - Service → **"Logs"** tab
   - Look for:
     ```
     ✓ Connected to SQL Server...
     ✓ Database connection successful
     Server running at http://0.0.0.0:10000
     ```

2. **Test Endpoints:**
   ```bash
   # Replace with your Render URL
   https://webinar-backend.onrender.com/send-otp
   ```

### Step 6: Update Frontend

Update `frontend/js/config.js`:

```javascript
const API_CONFIG = {
    environment: 'production',
    
    endpoints: {
        development: 'http://localhost:3000',
        production: 'https://your-backend.onrender.com'  // Your Render URL
    },
    
    getBaseURL() {
        return this.endpoints[this.environment];
    }
};
```

Or run the script:
```powershell
.\scripts\update-api-urls.ps1 -Environment prod
# Enter: https://your-backend.onrender.com
```

### Step 7: Deploy Frontend

1. **Create Static Site:**
   - Dashboard → **"New"** → **"Static Site"**
   - Connect repository: `needles_webinar`
   - Configure:
     - **Name:** `webinar-frontend`
     - **Branch:** `main`
     - **Root Directory:** Leave empty
     - **Build Command:** Leave empty
     - **Publish Directory:** `frontend`

2. **Click "Create Static Site"**

## 🔧 Configuration Details

### Required Python Packages

Your `backend/requirements-prod.txt` includes:
```
Flask==3.1.2
Flask-Cors==6.0.1
gunicorn==23.0.0
pyodbc==5.2.0
python-dotenv==1.1.0
razorpay==1.4.2
```

### Gunicorn Configuration

```bash
gunicorn run:app \
  --bind 0.0.0.0:$PORT \
  --timeout 120 \
  --workers 2
```

- **timeout 120:** Extended for database operations
- **workers 2:** Suitable for free tier

### Database Connection

Your SQL Server at `18.204.144.126` must:
- ✅ Allow connections from Render IPs
- ✅ Port 1433 open
- ✅ User `Appuser` has proper permissions

## 🔒 Security Checklist

- [ ] Use Razorpay **LIVE** keys (not test keys)
- [ ] Verify Amazon SES is in **production mode**
- [ ] Database credentials are **secure**
- [ ] Firewall allows Render IPs
- [ ] HTTPS enabled (Render provides free SSL)

## 📊 Database Firewall Settings

If connection fails, whitelist Render's IP ranges in your SQL Server firewall.

**Get Render's outbound IPs:**
- Render Shell → Run: `curl ifconfig.me`
- Add that IP to SQL Server firewall rules

## 🐛 Troubleshooting

### Error: "Module 'pyodbc' not found"

**Solution:** Check build logs. If ODBC driver missing:

Update `render.yaml` build command:
```yaml
buildCommand: |
  apt-get update
  apt-get install -y unixodbc-dev
  pip install -r backend/requirements-prod.txt
```

### Error: "Database connection failed"

**Solutions:**
1. Check environment variables are set correctly
2. Verify SQL Server allows remote connections
3. Test connection from Render Shell:
   ```bash
   python -c "from app.database import test_connection; test_connection()"
   ```

### Error: "Timeout during deployment"

**Solution:** Increase timeout in `render.yaml`:
```yaml
startCommand: cd backend && gunicorn run:app --bind 0.0.0.0:$PORT --timeout 300
```

### Error: "Port already in use"

Render assigns `$PORT` automatically. Ensure:
```python
# In run.py
PORT = int(os.getenv('PORT', 3000))
```

## 🎯 Post-Deployment

1. **Test Registration Flow:**
   - Visit your frontend URL
   - Complete registration
   - Verify OTP email
   - Test payment

2. **Monitor Logs:**
   - Check for database connections
   - Watch for errors
   - Monitor response times

3. **Verify Database:**
   - Connect to SQL Server
   - Check `registrations` table
   - Verify OTPs are stored

4. **Configure Webhooks:**
   - Razorpay Dashboard → Webhooks
   - Add URL: `https://your-backend.onrender.com/webhook`

## 📝 Environment Variables Quick Reference

| Variable | Example | Required |
|----------|---------|----------|
| FLASK_ENV | production | Yes |
| RAZORPAY_KEY_ID | rzp_live_xxxxx | Yes |
| RAZORPAY_KEY_SECRET | secret | Yes |
| RAZORPAY_WEBHOOK_SECRET | whsec_xxx | Yes |
| SMTP_USERNAME | AKIAW... | Yes |
| SMTP_PASSWORD | smtp_pass | Yes |
| VERIFIED_SENDER | your@email.com | Yes |
| DB_SERVER | 18.204.144.126 | Yes |
| DB_NAME | webinar_db | Yes |
| DB_USER | Appuser | Yes |
| DB_PASSWORD | db_password | Yes |

## 🚦 Health Check

Render will ping: `https://your-backend.onrender.com/success`

Make sure this endpoint exists and returns 200 OK.

## 💰 Pricing

**Free Tier Includes:**
- 750 hours/month web service
- Auto-sleep after 15 min inactivity
- Free SSL certificates
- Automatic deployments

**Note:** Free tier services sleep when inactive. First request after sleep takes ~30 seconds.

## 🔄 Auto-Deploy

Render automatically deploys when you push to GitHub:

```powershell
git add .
git commit -m "Update feature"
git push origin main
# Render deploys automatically
```

## 📞 Support

- Render Docs: https://render.com/docs
- Dashboard: https://dashboard.render.com
- Your Backend URL: Will be like `https://webinar-backend-xxxx.onrender.com`
- Your Frontend URL: Will be like `https://webinar-frontend.onrender.com`

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements-prod.txt` exists
- [ ] Render account created
- [ ] Backend service created
- [ ] All environment variables set
- [ ] Database tables initialized
- [ ] Frontend updated with backend URL
- [ ] Static site created
- [ ] Test complete registration flow
- [ ] Razorpay webhook configured
- [ ] Monitor logs for errors

---

**Your backend will be live at:** `https://webinar-backend-[random].onrender.com`

Update your frontend config with this URL and you're ready to go! 🎉
