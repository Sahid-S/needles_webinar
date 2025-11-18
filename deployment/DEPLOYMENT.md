# Render Deployment Guide

Complete step-by-step guide to deploy the webinar platform on Render.

## Prerequisites

- GitHub/GitLab repository with your code
- Render account (free tier available)
- Razorpay account with API keys
- Amazon SES credentials

## Option 1: Using render.yaml (Recommended)

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Connect to Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your repository
   - Render will detect `render.yaml` and configure everything

3. **Add environment variables in Render Dashboard:**
   - Go to your backend service
   - Click "Environment"
   - Add these variables:
     ```
     RAZORPAY_KEY_ID=rzp_live_xxxxx
     RAZORPAY_KEY_SECRET=your_secret
     RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
     SMTP_USERNAME=AKIAW3MEFEQHVDP73HEY
     SMTP_PASSWORD=your_smtp_password
     VERIFIED_SENDER=jamindustries.info@gmail.com
     ```

4. **Deploy:**
   - Click "Apply"
   - Wait for deployment to complete

## Option 2: Manual Deployment

### Step 1: Deploy Backend (Web Service)

1. **Create Web Service:**
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect your repository

2. **Configure Service:**
   - **Name:** `webinar-backend`
   - **Region:** Oregon (or closest to you)
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Runtime:** Python 3
   - **Build Command:**
     ```bash
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     cd backend && gunicorn run:app --bind 0.0.0.0:$PORT
     ```

3. **Add Environment Variables:**
   ```
   RAZORPAY_KEY_ID=rzp_live_RWvoJlAdc0Vh7T
   RAZORPAY_KEY_SECRET=your_secret_key
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   SMTP_USERNAME=AKIAW3MEFEQHVDP73HEY
   SMTP_PASSWORD=your_smtp_password
   VERIFIED_SENDER=jamindustries.info@gmail.com
   FLASK_ENV=production
   ```

4. **Create Service** and wait for deployment

5. **Note your backend URL:**
   - Example: `https://webinar-backend.onrender.com`

### Step 2: Update Frontend API Endpoints

1. **Edit `frontend/register.html`:**
   
   Replace all occurrences of `http://localhost:3000` with your Render backend URL:

   ```javascript
   // Find and replace these lines:
   const response = await fetch('http://localhost:3000/send-otp', {
   // Replace with:
   const response = await fetch('https://webinar-backend.onrender.com/send-otp', {

   // Do this for all endpoints:
   // - /send-otp
   // - /verify-otp
   // - /validate-contact
   // - /create-order
   // - /verify-payment
   ```

2. **Commit and push changes:**
   ```bash
   git add frontend/register.html
   git commit -m "Update API endpoints for production"
   git push
   ```

### Step 3: Deploy Frontend (Static Site)

1. **Create Static Site:**
   - Go to Render Dashboard
   - Click "New" → "Static Site"
   - Connect your repository

2. **Configure Site:**
   - **Name:** `webinar-frontend`
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Build Command:** (leave empty)
   - **Publish Directory:** `.`

3. **Create Site** and wait for deployment

4. **Note your frontend URL:**
   - Example: `https://webinar-frontend.onrender.com`

### Step 4: Configure Razorpay Webhook

1. **Go to Razorpay Dashboard:**
   - Navigate to Settings → Webhooks
   - Click "Create Webhook"

2. **Add Webhook URL:**
   ```
   https://webinar-backend.onrender.com/webhook
   ```

3. **Select Events:**
   - `payment.authorized`
   - `payment.captured`
   - `payment.failed`
   - `order.paid`

4. **Copy Webhook Secret:**
   - Save this secret
   - Add it to Render environment variables as `RAZORPAY_WEBHOOK_SECRET`

### Step 5: Test Deployment

1. **Visit your frontend URL**

2. **Test registration flow:**
   - Fill out the form
   - Request OTP
   - Check email for OTP
   - Verify OTP
   - Proceed to payment
   - Complete test payment

3. **Check backend logs:**
   - Go to Render Dashboard → Backend Service → Logs
   - Monitor for any errors

## Quick Script to Update API URLs

Run this in your terminal to update all API endpoints at once:

```bash
# For Windows PowerShell
$file = "frontend/register.html"
(Get-Content $file) -replace 'http://localhost:3000', 'https://webinar-backend.onrender.com' | Set-Content $file

# For Mac/Linux
sed -i '' 's|http://localhost:3000|https://webinar-backend.onrender.com|g' frontend/register.html
```

## Environment Variables Reference

| Variable | Where to Get | Example |
|----------|--------------|---------|
| `RAZORPAY_KEY_ID` | Razorpay Dashboard → API Keys | `rzp_live_xxxxx` |
| `RAZORPAY_KEY_SECRET` | Razorpay Dashboard → API Keys | `your_secret_key` |
| `RAZORPAY_WEBHOOK_SECRET` | Razorpay Dashboard → Webhooks | `webhook_secret` |
| `SMTP_USERNAME` | AWS SES Console → SMTP Settings | `AKIAW3MExxxxx` |
| `SMTP_PASSWORD` | AWS SES Console → SMTP Settings | `smtp_password` |
| `VERIFIED_SENDER` | Your verified email in SES | `your@email.com` |

## Troubleshooting

### Backend Issues

1. **Service won't start:**
   - Check logs in Render Dashboard
   - Verify all environment variables are set
   - Check Python version in `runtime.txt`

2. **Import errors:**
   - Ensure `gunicorn` is in `requirements.txt`
   - Check file paths are correct

3. **Database/Storage issues:**
   - Render's free tier has ephemeral filesystem
   - Use external database for persistent storage

### Frontend Issues

1. **CORS errors:**
   - Ensure `flask-cors` is installed
   - Backend has `CORS(app)` enabled

2. **API not connecting:**
   - Check backend URL is correct
   - Verify backend service is running
   - Check browser console for errors

3. **Payment not working:**
   - Verify Razorpay keys in environment
   - Check webhook URL is configured
   - Test with test mode keys first

### Email Issues

1. **OTP not sending:**
   - Verify SES credentials
   - Check sender email is verified in SES
   - Review backend logs for SMTP errors

## Free Tier Limitations

Render Free Tier includes:
- ✅ 750 hours/month (enough for one service 24/7)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Services spin down after 15 min inactivity
- ⚠️ First request after inactivity takes ~30 seconds

For production, consider upgrading to Starter plan ($7/month).

## Monitoring

1. **Backend Health:**
   - Visit: `https://your-backend.onrender.com/success`
   - Should return HTML success page

2. **Check Logs:**
   - Render Dashboard → Service → Logs
   - Monitor for errors and warnings

3. **Set Up Alerts:**
   - Render Dashboard → Service → Settings → Notifications
   - Get notified of deployment failures

## Next Steps After Deployment

- [ ] Test complete user flow
- [ ] Update Razorpay webhook
- [ ] Test email delivery
- [ ] Test payment processing
- [ ] Set up custom domain (optional)
- [ ] Enable monitoring/alerts
- [ ] Create backup strategy
- [ ] Document API endpoints
- [ ] Set up CI/CD pipeline

## Support

If you encounter issues:
1. Check Render logs
2. Review backend error messages
3. Test locally first
4. Check environment variables
5. Verify external services (Razorpay, SES)

## Security Checklist

Before going live:
- [ ] All API keys in environment variables (not hardcoded)
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled (automatic on Render)
- [ ] Webhook signature verification enabled
- [ ] Rate limiting configured (optional)
- [ ] Input validation on all forms
- [ ] CORS properly configured
