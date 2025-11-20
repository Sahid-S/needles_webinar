# 🎯 Dynamic Webinar Settings Feature

## Overview

The admin can now set the webinar date and time, which automatically updates across the entire website.

## What's New

### Database
- **New Table:** `settings` - Stores webinar configuration
  - `webinar_date` - e.g., "December 10, 2025"
  - `webinar_time` - e.g., "9:00 AM - 12:00 PM IST"
  - `webinar_title` - e.g., "The Needles Webinar"
  - `zoom_link` - Saved Zoom link for quick access

### Backend APIs

#### 1. GET `/webinar-info` (Public)
Returns webinar date, time, and title for display on frontend pages.

**Response:**
```json
{
  "success": true,
  "webinar_date": "December 10, 2025",
  "webinar_time": "9:00 AM - 12:00 PM IST",
  "webinar_title": "The Needles Webinar"
}
```

#### 2. GET `/admin/webinar-settings` (Admin Only)
Get all webinar settings including zoom_link.

**Headers Required:**
```
X-Admin-Token: <admin_token>
```

**Response:**
```json
{
  "success": true,
  "settings": {
    "webinar_date": "December 10, 2025",
    "webinar_time": "9:00 AM - 12:00 PM IST",
    "webinar_title": "The Needles Webinar",
    "zoom_link": "https://zoom.us/j/1234567890"
  }
}
```

#### 3. POST `/admin/webinar-settings` (Admin Only)
Update webinar settings.

**Headers Required:**
```
X-Admin-Token: <admin_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "webinar_date": "December 15, 2025",
  "webinar_time": "10:00 AM - 1:00 PM IST",
  "webinar_title": "Fashion Business Masterclass",
  "zoom_link": "https://zoom.us/j/9876543210"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Webinar settings updated successfully",
  "settings": { ... }
}
```

---

## Admin Panel Updates

### New Section: ⚙️ Webinar Settings

Located at the top of the admin dashboard, this section allows you to:

1. **Update Webinar Date** - Changes what appears on registration page
2. **Update Webinar Time** - Changes what appears on registration page
3. **Update Webinar Title** - For future use
4. **Save Zoom Link** - Auto-fills when sending emails

**Features:**
- Auto-fills the "Send Webinar Zoom Link" form below
- Updates persist in database
- Changes reflect immediately on frontend

---

## Frontend Integration

### `index.html`
- FAQ section dynamically loads webinar date/time
- Falls back to default if API fails

### `register.html`
- Can be updated to show dynamic date/time (optional)

### `admin.html`
- Settings form loads current values on login
- Saves changes to database
- Auto-populates email sending form

---

## How to Use

### Step 1: Set Webinar Details
1. Login to admin panel: `http://localhost:8000/admin.html`
2. Find the "⚙️ Webinar Settings" section at the top
3. Fill in:
   - **Webinar Date:** e.g., "December 15, 2025"
   - **Webinar Time:** e.g., "10:00 AM - 1:00 PM IST"
   - **Zoom Link:** e.g., "https://zoom.us/j/1234567890"
4. Click **"💾 Save Webinar Settings"**

### Step 2: Verify Changes
1. Open `http://localhost:8000/index.html`
2. Scroll to FAQ section
3. Check "When is the webinar scheduled?" - should show your new date/time

### Step 3: Send Emails
1. In admin panel, the "Send Webinar Zoom Link" form will be pre-filled with your settings
2. Just click "Send Zoom Links to All Participants"
3. Emails will use the date/time you configured

---

## Database Setup

The settings table was created automatically. To verify or manually create:

```sql
-- Check if table exists
SELECT * FROM settings;

-- Insert default values (if needed)
INSERT INTO settings (setting_key, value) VALUES 
('webinar_date', 'December 10, 2025'),
('webinar_time', '9:00 AM - 12:00 PM IST'),
('webinar_title', 'The Needles Webinar'),
('zoom_link', '');
```

---

## Files Modified

### Backend:
- ✅ `backend/app/models/settings.py` - New Settings model
- ✅ `backend/app/routes/public.py` - New public endpoint
- ✅ `backend/app/routes/admin.py` - Added webinar settings management
- ✅ `backend/app/__init__.py` - Registered public blueprint
- ✅ `backend/create_settings_table.py` - Setup script

### Frontend:
- ✅ `frontend/admin.html` - Added settings form and management
- ✅ `frontend/index.html` - Dynamic date/time loading

### Database:
- ✅ New table: `settings` with initial data

---

## Testing Checklist

### Backend Tests:
- [ ] GET `/webinar-info` returns default values
- [ ] GET `/admin/webinar-settings` requires authentication
- [ ] POST `/admin/webinar-settings` updates database
- [ ] Settings persist after server restart

### Frontend Tests:
- [ ] Admin can login and see settings form
- [ ] Settings form loads current values
- [ ] Saving settings shows success message
- [ ] Send links form auto-fills with saved zoom link
- [ ] Index page FAQ shows dynamic date/time

### Integration Tests:
- [ ] Change date in admin → Verify on index page
- [ ] Change time in admin → Verify on index page
- [ ] Save zoom link → Verify it auto-fills in send form
- [ ] Settings survive server restart

---

## Future Enhancements

### Recommended:
1. **Registration Fee** - Make ₹299 configurable via settings
2. **Webinar Description** - Rich text editor for main content
3. **Multiple Webinars** - Support for recurring events
4. **Email Templates** - Customizable email content
5. **Branding** - Logo and colors in settings

### Optional:
- Timezone support
- Calendar integration (.ics file generation)
- Reminder emails (auto-send X days before)
- Settings history/audit log

---

## Troubleshooting

### Settings not saving
```bash
# Check if settings table exists
python -c "from app import create_app; from app.models.settings import Settings; app = create_app(); app.app_context().push(); print(Settings.get_all_settings())"
```

### Frontend not updating
- Clear browser cache
- Check browser console for errors
- Verify API URL is correct (localhost:3000)

### Database errors
```bash
# Recreate settings table
cd backend
python create_settings_table.py
```

---

## Security Notes

✅ **Public endpoint** (`/webinar-info`) - No authentication required  
✅ **Admin endpoints** (`/admin/webinar-settings`) - Token authentication required  
✅ **Zoom link** - NOT exposed in public endpoint  

---

**Created:** November 19, 2025  
**Status:** ✅ Implemented and ready for testing  
**Next:** Restart backend server and test the feature!
