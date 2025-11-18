# 🚀 Deploy Backend to Render - Quick Guide

## Step 1: Push Your Code to GitHub

```powershell
# If not initialized yet
git init
git add .
git commit -m "Backend ready for Render deployment"
git branch -M main
git remote add origin https://github.com/Sahid-S/needles_webinar.git
git push -u origin main

# If already initialized
git add .
git commit -m "Backend ready for Render deployment"
git push origin main
```

## Step 2: Go to Render

1. Open https://render.com
2. Sign in with GitHub
3. Authorize Render to access your repository

## Step 3: Create Web Service

### Option A: Using Blueprint (Easiest)

1. Click **"New"** → **"Blueprint"**
2. Select repository: **`needles_webinar`**
3. Render detects `deployment/render.yaml`
4. Click **"Apply"**
5. Wait for service creation (~30 seconds)

### Option B: Manual Creation

1. Click **"New"** → **"Web Service"**
2. Connect repository: **`needles_webinar`**
3. Configure:
   - **Name:** `webinar-backend`
   - **Region:** Oregon (or closest to you)
   - **Branch:** `main`
   - **Root Directory:** *leave empty*
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r backend/requirements-prod.txt`
   - **Start Command:** `cd backend && gunicorn run:app --bind 0.0.0.0:$PORT --timeout 120 --workers 2`
   - **Instance Type:** Free
4. Click **"Create Web Service"**

## Step 4: Add Environment Variables

Go to **Environment** tab and add these:

```
FLASK_ENV=production
RAZORPAY_KEY_ID=your_live_razorpay_key_id
RAZORPAY_KEY_SECRET=your_live_razorpay_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
VERIFIED_SENDER=jamindustries.info@gmail.com
DB_SERVER=18.204.144.126
DB_NAME=webinar_db
DB_USER=Appuser
DB_PASSWORD=your_database_password
```

Click **"Save Changes"** - Render will redeploy automatically.

## Step 5: Wait for Deployment

Watch the **Logs** tab. You should see:
```
Building...
Installing dependencies...
Starting server...
✓ Connected to SQL Server...
✓ Database connection successful
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:10000
```

Your backend URL will be: `https://webinar-backend-xxxx.onrender.com`

## Step 6: Initialize Database Tables

**IMPORTANT: Run this ONCE after first deployment**

Go to **Shell** tab and run:
```bash
cd backend
python init_db.py
```

You should see:
```
✓ Connected to SQL Server...
✓ Database tables initialized successfully
```

## Step 7: Test Your Backend

```bash
# Test health endpoint
curl https://your-backend-url.onrender.com/success

# Test send OTP
curl -X POST https://your-backend-url.onrender.com/send-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

## Step 8: Update Frontend

Update `frontend/js/config.js` with your Render URL:

```javascript
const API_CONFIG = {
    environment: 'production',
    endpoints: {
        development: 'http://localhost:3000',
        production: 'https://webinar-backend-xxxx.onrender.com'  // Your actual URL
    }
};
```

Or use the script:
```powershell
.\scripts\update-api-urls.ps1 -Environment prod
# Enter your Render URL when prompted
```

## Step 9: Test Complete Flow

1. Open `frontend/index.html` locally
2. Try registration flow
3. Verify OTP email arrives
4. Complete payment

## ✅ You're Done!

Your backend is live at: `https://webinar-backend-xxxx.onrender.com`

## 🔧 Common Issues

### Issue: "Module 'pyodbc' not found"
**Solution:** Check that `backend/requirements-prod.txt` is being used in build command.

### Issue: "Database connection failed"
**Solutions:**
1. Verify environment variables are correct
2. Check SQL Server firewall allows Render's IP
3. In Render Shell, test: `python -c "from app.database import test_connection; test_connection()"`

### Issue: "502 Bad Gateway"
**Solution:** Check logs for Python errors. Service might still be starting.

### Issue: "Free tier sleeping"
**Expected:** Free tier sleeps after 15 min. First request wakes it (~30 sec delay).

## 📝 Next Steps

1. Configure Razorpay webhook: `https://your-backend-url.onrender.com/webhook`
2. Test payment flow end-to-end
3. Monitor logs for any errors
4. Deploy frontend separately (optional)

## 🆘 Need Help?

- Check full logs in Render dashboard
- Verify all environment variables
- Test database connection from Shell tab
- Check `deployment/RENDER_DEPLOYMENT.md` for detailed troubleshooting

---

**Your Backend API will be accessible at:**
`https://webinar-backend-[random].onrender.com`

Save this URL and update your frontend config! 🎉
