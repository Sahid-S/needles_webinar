# SQL Server Connection - Quick Start

## ✅ What Was Done

1. **Created database module** (`backend/app/database.py`)
   - Connection management with pyodbc
   - Context managers for safe operations
   - Auto table creation scripts

2. **Created models** (`backend/app/models.py`)
   - Registration model
   - OTP model
   - Payment model

3. **Updated OTP system** to use database instead of memory

4. **Created initialization script** (`backend/init_db.py`)

## 🚀 Quick Setup (5 steps)

### 1. Open SSMS and create database:
```sql
CREATE DATABASE webinar_db;
```

### 2. Update `backend/.env`:
```env
DB_SERVER=localhost
DB_NAME=webinar_db
DB_USER=sa
DB_PASSWORD=your_actual_password
```

### 3. Run initialization:
```powershell
cd backend
python init_db.py
```

### 4. Start server:
```powershell
python run.py
```

### 5. Test - you should see:
```
✓ Connected to SQL Server...
✓ Database connection successful
```

## 📊 View Your Data in SSMS

```sql
-- View all registrations
SELECT * FROM registrations;

-- View active OTPs
SELECT * FROM otp_verification WHERE expiry > GETDATE();

-- View payments
SELECT * FROM payments;
```

## 🔧 Common Connection Strings

**Localhost with SA:**
```env
DB_SERVER=localhost
DB_USER=sa
```

**SQL Express:**
```env
DB_SERVER=localhost\SQLEXPRESS
DB_USER=sa
```

**Custom User:**
```env
DB_SERVER=localhost
DB_USER=webinar_user
```

## 📖 Full Documentation

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for:
- Detailed setup instructions
- Troubleshooting guide
- Database schema
- SQL queries
- Windows Authentication setup

## 🎯 What Changed

**Before:** OTPs stored in memory (lost on restart)  
**After:** OTPs stored in SQL Server (persistent)

**New Features:**
- Persistent data storage
- Registration history
- Payment tracking
- Better scalability

## 💡 Next Steps

1. Complete database setup
2. Test registration flow
3. View data in SSMS
4. Backup database regularly
