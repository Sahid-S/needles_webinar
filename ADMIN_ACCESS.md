# Admin Panel Access

## Login Credentials

**URL:** `http://localhost:8000/admin-login.html`

### Default Credentials:

**Option 1:**
- Username: `admin`
- Password: `needles_admin_2025`

**Option 2:**
- Username: `needles_admin`
- Password: `needles_admin_2025`

## Features

### 📊 Dashboard Statistics
- Total Registrations
- Paid Registrations
- Pending Payments

### 📧 Send Webinar Links
- Send Zoom link to all paid participants
- Customize webinar date and time
- Track email delivery status

### 👥 View Registrations
- Complete list of all registrations
- Payment status for each participant
- Registration timestamps
- Participant details (name, email, phone, city)

## Security Notes

⚠️ **IMPORTANT FOR PRODUCTION:**

1. **Change the default password** in `admin-login.html`
2. **Move authentication to backend** - current implementation is client-side only
3. **Use environment variables** for the admin key
4. **Implement proper session management**
5. **Add rate limiting** to prevent brute force attacks
6. **Use HTTPS** in production

## How to Use

1. Navigate to homepage footer
2. Click the small "🔐 Admin" link
3. Enter credentials
4. Access admin dashboard
5. Send Zoom links or view registrations

## API Endpoints Used

- `GET /admin/registrations?admin_key=XXX` - Fetch all registrations
- `POST /admin/send-webinar-links` - Send emails to all paid participants

## Customization

To change credentials, edit `frontend/admin-login.html`:

```javascript
const validCredentials = {
    'your_username': 'your_admin_key',
    'another_user': 'another_admin_key'
};
```

Make sure the `admin_key` matches the one set in `backend/app/routes/admin.py`.
