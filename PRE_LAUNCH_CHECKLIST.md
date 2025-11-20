# ⚠️ Pre-Launch Checklist - The Needles Webinar

## ✅ What's Working

### Backend (Port 3000)
- ✅ Flask server configured
- ✅ SQL Server database connected (TheNeedles)
- ✅ All API routes functional
- ✅ Email service (Amazon SES) configured
- ✅ Razorpay payment integration (Test Mode)
- ✅ OTP verification system
- ✅ Admin panel API endpoints

### Frontend (Port 8000)
- ✅ Registration form with validation
- ✅ Email OTP verification
- ✅ Phone number with +91 prefix
- ✅ Razorpay payment gateway (₹1 test)
- ✅ Success/failure pages
- ✅ Admin panel with login
- ✅ Webinar link email system

### Database Tables
- ✅ registrations (stores user data)
- ✅ otp_verification (email OTP)
- ✅ payments (payment records)

---

## ⚠️ CRITICAL ISSUES TO FIX BEFORE LAUNCH

### 1. **Payment Amount - CURRENTLY ₹1**
**Location:** `frontend/register.html` line ~757
```javascript
const paymentAmount = 100; // ₹1 in paise (change to 29900 for ₹299)
```
**Action:** Change to `29900` for ₹299 registration fee

**Also Update Display:** Line ~206
```html
<div class="payment-amount">₹299</div>
```
Make sure this matches actual amount being charged.

---

### 2. **Razorpay Test Mode Keys**
**Location:** `backend/.env`
```
RAZORPAY_KEY_ID=rzp_test_Rh6He9b7BGzzQa
RAZORPAY_KEY_SECRET=cggP4fmR4Bvh7Izz3BCVe24q
```
**Action:** 
- Switch to LIVE keys before launch
- Get live keys from Razorpay Dashboard → Settings → API Keys
- Update both `.env` and `frontend/register.html` (line ~797)

---

### 3. **Razorpay Payment Methods**
**Issue:** Test mode may not have payment methods enabled
**Action:**
1. Go to Razorpay Dashboard (Test Mode for now)
2. Settings → Configuration → Payment Methods
3. Enable:
   - ✅ Credit/Debit Cards
   - ✅ UPI
   - ✅ Netbanking
   - ✅ Wallets (optional)

**For LIVE mode:** Repeat above steps in live mode before launch

---

### 4. **Admin Panel Security**
**Location:** `frontend/admin.html` line ~473
```javascript
const validCredentials = {
    'admin': 'needles_admin_2025',
    'needles_admin': 'needles_admin_2025'
};
```
**Issues:**
- ⚠️ Credentials hardcoded in frontend (anyone can see in browser)
- ⚠️ No backend validation
- ⚠️ Simple password

**MUST DO FOR PRODUCTION:**
1. Move authentication to backend
2. Use stronger passwords
3. Hash passwords
4. Implement JWT or session tokens
5. Add rate limiting for login attempts

**Quick Fix (if rushing):**
- Change password to something stronger
- Obfuscate the JavaScript code
- But still plan to move to backend auth ASAP

---

### 5. **Email Contact Information**
**Location:** Multiple email templates in `backend/app/utils/email_service.py`

**Lines to update:**
- Line ~97: `📧 Email: support@theneedles.com`
- Line ~98: `📱 WhatsApp: +91 XXXXX XXXXX`
- Line ~221: `📧 Email: support@theneedles.com`
- Line ~222: `📱 WhatsApp: +91 XXXXX XXXXX`

**Action:** Replace with actual support contact details

---

### 6. **Webinar Date & Time**
**Current:** December 10, 2025 | 9:00 AM - 12:00 PM IST

**Update in:**
1. `frontend/register.html` - Multiple locations
2. Email templates in `backend/app/utils/email_service.py`
3. Admin panel default values

**Verify:** All dates are consistent across the application

---

### 7. **Database Backup**
**Action:** Set up automatic backups for SQL Server database
- User registrations
- Payment records
- OTP data

---

### 8. **Environment Variables**
**Location:** `backend/.env`

**NEVER commit this file to GitHub!**

Check `.gitignore` includes:
```
.env
*.env
```

**For production deployment:**
- Store in secure environment variables
- Use different credentials for production

---

### 9. **CORS Configuration**
**Location:** `backend/app/__init__.py`

**Current:** Allows all origins (for development)
```python
CORS(app)
```

**For Production:**
```python
CORS(app, origins=['https://yourdomain.com'])
```

---

### 10. **Duplicate Email Registration**
**Status:** ✅ Handled (uses existing registration if email exists)

But consider:
- Should duplicate emails be allowed?
- Should users get a warning?
- Should they be redirected to login?

---

## 🔧 RECOMMENDED IMPROVEMENTS

### 1. **Email Verification Required**
Currently users can skip OTP if they manipulate the frontend.

**Fix:** Backend should check if email is verified before accepting payment.

### 2. **Payment Webhook**
**Location:** `backend/app/routes/payment.py` - webhook endpoint exists but not configured

**Action:**
1. Go to Razorpay Dashboard → Webhooks
2. Add webhook URL: `https://yourdomain.com/webhook`
3. Add webhook secret to `.env`
4. Enable events:
   - `payment.captured`
   - `payment.failed`
   - `order.paid`

**Why:** Ensures payment status is updated even if user closes browser

### 3. **SSL/HTTPS**
**Critical for Production:**
- Payment pages MUST use HTTPS
- Get SSL certificate for your domain
- Razorpay may block HTTP sites

### 4. **Error Logging**
Consider adding proper logging:
- Payment failures
- Email delivery failures
- Database errors

Tools: Sentry, LogRocket, or simple file logging

### 5. **Rate Limiting**
Add rate limiting to prevent:
- OTP spam
- Payment spam
- Admin brute force

### 6. **Terms & Conditions**
**Location:** `frontend/pages/terms-conditions.html`
**Action:** Update with actual legal terms

Same for:
- Privacy Policy
- Refund Policy

### 7. **Success/Failure URLs**
**Current:** Redirects to local pages
**Action:** Ensure URLs work after deployment

---

## 🚀 PRE-LAUNCH TESTING CHECKLIST

### Test Complete Flow:
- [ ] Register with valid email
- [ ] Receive OTP email
- [ ] Verify OTP
- [ ] Fill all form fields
- [ ] Complete payment with test card
- [ ] Verify confirmation email received
- [ ] Check database for registration
- [ ] Test admin login
- [ ] Send webinar link from admin panel
- [ ] Verify webinar link email received

### Test Edge Cases:
- [ ] Invalid OTP
- [ ] Expired OTP
- [ ] Payment failure
- [ ] Duplicate email registration
- [ ] Invalid phone numbers
- [ ] Empty form fields
- [ ] Network interruptions

### Security Testing:
- [ ] SQL injection attempts
- [ ] XSS attempts
- [ ] CSRF tokens (not implemented - consider adding)
- [ ] Admin panel unauthorized access

---

## 📝 DEPLOYMENT CHECKLIST

### Before Going Live:
1. [ ] Change payment amount to actual (₹299)
2. [ ] Switch to Razorpay LIVE keys
3. [ ] Update all email contact information
4. [ ] Verify webinar date/time everywhere
5. [ ] Enable Razorpay payment methods (LIVE mode)
6. [ ] Set up SSL certificate
7. [ ] Configure CORS for production domain
8. [ ] Set up database backups
9. [ ] Configure Razorpay webhooks
10. [ ] Update admin credentials
11. [ ] Test on production environment
12. [ ] Monitor error logs

### Post-Launch:
1. [ ] Monitor registrations in real-time
2. [ ] Check email delivery success rate
3. [ ] Monitor payment success/failure rate
4. [ ] Have support contact ready for issues
5. [ ] Test sending webinar links 24hrs before event

---

## 🆘 QUICK FIXES FOR COMMON ISSUES

### Emails Not Sending
- Check SMTP credentials in `.env`
- Verify sender email in Amazon SES
- Check spam folder

### Payment Failing
- Verify Razorpay keys are correct
- Check if payment methods enabled
- Ensure amount is in paise (multiply by 100)
- Test with Razorpay test cards

### Database Connection Failed
- Check SQL Server is running
- Verify DB credentials
- Check if IP is whitelisted
- Test connection string

### Admin Panel Not Loading
- Check backend is running
- Verify CORS settings
- Check browser console for errors

---

## 💡 PERFORMANCE OPTIMIZATION (Optional)

- Add loading states for all API calls
- Implement request caching
- Optimize email templates (currently quite large)
- Add CDN for static assets
- Minify JavaScript/CSS
- Compress images

---

## 📊 MONITORING RECOMMENDATIONS

Track these metrics:
- Registration conversion rate
- Payment success rate
- Email delivery rate
- Average time to complete registration
- Most common errors
- Browser/device usage

---

## 🔗 IMPORTANT URLs TO BOOKMARK

- Razorpay Dashboard: https://dashboard.razorpay.com
- Amazon SES Console: https://console.aws.amazon.com/ses
- SQL Server Management: (your connection)
- Admin Panel: http://yourdomain.com/admin.html

---

## 📞 EMERGENCY CONTACTS

Have these ready on launch day:
- Technical support person (you!)
- Razorpay support: support@razorpay.com
- Database administrator
- Email service support

---

## ✨ WHAT'S ALREADY GREAT

- Clean, professional UI
- Mobile responsive design
- Proper error handling
- Duplicate prevention
- Email confirmations
- Admin panel for management
- Database persistence
- Payment gateway integration

---

**Last Updated:** November 19, 2025
**Next Review:** Before switching to LIVE mode
