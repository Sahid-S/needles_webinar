# 🚀 Quick Render Deployment Checklist

## ✅ Pre-Deployment (Do This First)

```powershell
# 1. Commit and push your code
git add .
git commit -m "Ready for Render deployment"
git push origin main

# 2. Verify production requirements file exists
# Check: backend/requirements-prod.txt ✓
```

## 🌐 On Render.com

### 1. Create Account
- Go to: https://render.com
- Sign up with GitHub
- Connect repository: `Sahid-S/needles_webinar`

### 2. Deploy Backend

**Dashboard → New → Blueprint**
- Select your repository
- Render detects `deployment/render.yaml`
- Click **"Apply"**

### 3. Add Environment Variables

**Your Service → Environment → Add Environment Variables:**

```
FLASK_ENV=production
RAZORPAY_KEY_ID=your_live_key
RAZORPAY_KEY_SECRET=your_live_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
SMTP_USERNAME=your_smtp_user
SMTP_PASSWORD=your_smtp_pass
VERIFIED_SENDER=jamindustries.info@gmail.com
DB_SERVER=18.204.144.126
DB_NAME=webinar_db
DB_USER=Appuser
DB_PASSWORD=your_db_password
```

Click **"Save Changes"**

### 4. Wait for Deployment
- Watch **Logs** tab
- Look for: ✓ Database connection successful
- Get your URL: `https://webinar-backend-xxxx.onrender.com`

### 5. Initialize Database (ONE TIME ONLY)
- Go to **Shell** tab
- Run:
```bash
cd backend
python init_db.py
```

### 6. Deploy Frontend
**Dashboard → New → Static Site**
- Repository: `needles_webinar`
- Publish Directory: `frontend`
- Click **"Create Static Site"**

### 7. Update Frontend with Backend URL

Update `frontend/js/config.js`:
```javascript
production: 'https://webinar-backend-xxxx.onrender.com'  // Your actual URL
```

Then push:
```powershell
git add .
git commit -m "Update production API URL"
git push origin main
```

## 🎯 Final Checks

- [ ] Backend is live and healthy
- [ ] Database tables created
- [ ] Frontend can reach backend
- [ ] Test: Send OTP works
- [ ] Test: Verify OTP works
- [ ] Test: Payment flow works
- [ ] Razorpay webhook configured

## 📍 Your URLs

**Backend API:** https://webinar-backend-[random].onrender.com
**Frontend:** https://webinar-frontend.onrender.com

## 🆘 If Something Fails

Check `deployment/RENDER_DEPLOYMENT.md` for detailed troubleshooting!

## 💡 Quick Tips

- Free tier sleeps after 15 min → first request slow
- Check **Logs** tab for errors
- Environment variables need **Save Changes** click
- Auto-deploys on every git push

---

**Need help?** Check the full guide: `deployment/RENDER_DEPLOYMENT.md`
