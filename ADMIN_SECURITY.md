# 🔐 Admin Panel Security Update

## What Changed?

The admin panel has been **secured** by moving authentication from client-side to server-side.

### Before (Insecure ❌)
- Credentials hardcoded in frontend JavaScript
- Anyone could view credentials in browser DevTools
- No backend validation

### After (Secure ✅)
- Backend authentication API validates credentials
- Credentials stored in `.env` file (not in frontend)
- Token-based authentication with headers
- Session management with expiration handling

---

## How It Works Now

### 1. **Login Flow**
```
User enters credentials → Frontend sends to /auth/login API → 
Backend validates → Returns secure token → 
Token stored in sessionStorage → Used for all admin requests
```

### 2. **Authentication**
- All admin API calls now require `X-Admin-Token` header
- Token is validated on backend for every request
- Invalid/expired tokens return 401 Unauthorized

### 3. **Environment Variables**
Added to `backend/.env`:
```env
ADMIN_PASSWORD_HASH=needles_admin_2025
ADMIN_SECRET_KEY=needles_admin_secret_2025
```

---

## Current Credentials

### Development Mode:
- **Username:** `needles_admin`
- **Password:** `needles_admin_2025`

⚠️ **IMPORTANT:** These are temporary credentials for development/testing.

---

## Before Production Launch

### 1. **Change Passwords**
Update in `backend/.env`:
```env
ADMIN_PASSWORD_HASH=your_strong_password_here
ADMIN_SECRET_KEY=long_random_secret_key_here
```

### 2. **Generate Secure Token**
```python
# Run this in Python to generate a secure random key:
import secrets
print(secrets.token_urlsafe(32))
```

### 3. **Hash Passwords (Recommended)**
```python
from werkzeug.security import generate_password_hash

password = "your_new_strong_password"
hashed = generate_password_hash(password)
print(hashed)  # Put this in ADMIN_PASSWORD_HASH
```

Then update `backend/app/routes/auth.py` line 15 to use only hashed passwords:
```python
# Remove the plain text comparison, keep only:
is_valid = check_password_hash(stored_hash, password)
```

---

## API Endpoints

### POST `/auth/login`
**Request:**
```json
{
  "username": "needles_admin",
  "password": "needles_admin_2025"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "needles_admin_secret_2025",
  "username": "needles_admin"
}
```

**Response (Failure):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

---

### POST `/auth/verify`
Verify if token is still valid.

**Headers:**
```
X-Admin-Token: needles_admin_secret_2025
```

**Response:**
```json
{
  "success": true,
  "message": "Token is valid"
}
```

---

### GET `/admin/registrations`
Get all registrations (requires authentication).

**Headers:**
```
X-Admin-Token: needles_admin_secret_2025
```

---

### POST `/admin/send-webinar-links`
Send webinar links to all paid registrants (requires authentication).

**Headers:**
```
Content-Type: application/json
X-Admin-Token: needles_admin_secret_2025
```

**Body:**
```json
{
  "zoom_link": "https://zoom.us/j/xxxxx",
  "webinar_date": "December 10, 2025",
  "webinar_time": "9:00 AM - 12:00 PM IST"
}
```

---

## Security Features

### ✅ Implemented
- Backend credential validation
- Token-based authentication
- Secure token storage (sessionStorage)
- Session expiration handling
- Protected admin endpoints
- No credentials in frontend code

### 🔄 Recommended for Production
- [ ] Password hashing (bcrypt/pbkdf2)
- [ ] JWT tokens with expiration
- [ ] Rate limiting on login attempts
- [ ] HTTPS only (SSL certificate)
- [ ] Secure httpOnly cookies instead of sessionStorage
- [ ] Multi-factor authentication (optional)
- [ ] IP whitelisting for admin panel (optional)
- [ ] Audit logging for admin actions

---

## Testing

### Test Login:
1. Go to `http://localhost:8000/admin.html`
2. Username: `needles_admin`
3. Password: `needles_admin_2025`
4. Should successfully login and show dashboard

### Test Authentication:
```javascript
// In browser console after login:
console.log(sessionStorage.getItem('admin_key'));
// Should show: needles_admin_secret_2025
```

### Test API Protection:
```bash
# Without token - should fail:
curl http://localhost:3000/admin/registrations

# With token - should succeed:
curl -H "X-Admin-Token: needles_admin_secret_2025" http://localhost:3000/admin/registrations
```

---

## Files Changed

1. **`backend/app/routes/auth.py`** - New authentication endpoint
2. **`backend/app/routes/admin.py`** - Added `@verify_admin_token` decorator
3. **`backend/app/__init__.py`** - Registered auth blueprint
4. **`backend/.env`** - Added admin credentials
5. **`frontend/admin.html`** - Updated to use API authentication

---

## Troubleshooting

### Login fails with "Unauthorized"
- Check backend server is running on port 3000
- Verify credentials match `.env` file
- Check browser console for errors

### "Session expired" message
- Token might be invalid
- Clear sessionStorage: `sessionStorage.clear()`
- Try logging in again

### 401 Errors on admin actions
- Token not being sent in headers
- Check browser DevTools → Network → Headers
- Verify `X-Admin-Token` is present

---

**Created:** November 19, 2025  
**Status:** ✅ Implemented - Ready for testing  
**Next Step:** Test thoroughly, then implement password hashing before production
