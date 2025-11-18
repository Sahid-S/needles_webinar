# SQL Server Database Setup Guide

## Prerequisites

1. **SQL Server Management Studio (SSMS)** installed
2. **ODBC Driver 17 for SQL Server** installed
   - Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Or check if installed: Run `odbcad32.exe` → Drivers tab

## Step 1: Create Database in SSMS

Open SSMS and run this SQL script:

```sql
-- Create database
CREATE DATABASE webinar_db;
GO

-- Use the database
USE webinar_db;
GO

-- Verify creation
SELECT name FROM sys.databases WHERE name = 'webinar_db';
```

## Step 2: Create SQL Server Login (if needed)

If you want to create a specific user for the application:

```sql
-- Create login
CREATE LOGIN webinar_user WITH PASSWORD = 'YourStrongPassword123!';
GO

-- Create user in database
USE webinar_db;
CREATE USER webinar_user FOR LOGIN webinar_user;
GO

-- Grant permissions
ALTER ROLE db_owner ADD MEMBER webinar_user;
GO
```

## Step 3: Configure Backend Environment

Edit `backend/.env` file (copy from `.env.example` if needed):

```env
# SQL Server Database Configuration
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_SERVER=localhost
# Or use: DB_SERVER=localhost\SQLEXPRESS
# Or use: DB_SERVER=YOUR_COMPUTER_NAME\SQLEXPRESS
DB_NAME=webinar_db
DB_USER=sa
# Or use your custom user: DB_USER=webinar_user
DB_PASSWORD=your_actual_password
```

### Connection String Options:

**Option 1: Using SA account (localhost)**
```env
DB_SERVER=localhost
DB_USER=sa
DB_PASSWORD=your_sa_password
```

**Option 2: Using SQL Express (default instance)**
```env
DB_SERVER=localhost\SQLEXPRESS
DB_USER=sa
DB_PASSWORD=your_sa_password
```

**Option 3: Using custom user**
```env
DB_SERVER=localhost
DB_USER=webinar_user
DB_PASSWORD=YourStrongPassword123!
```

**Option 4: Using Windows Authentication**
For Windows Authentication, modify `backend/app/database.py`:
```python
connection_string = (
    f"DRIVER={{{config['DB_DRIVER']}}};"
    f"SERVER={config['DB_SERVER']};"
    f"DATABASE={config['DB_NAME']};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
```

## Step 4: Initialize Database Tables

Run the initialization script:

```powershell
cd backend
python init_db.py
```

You should see:
```
=== Database Initialization ===

1. Testing database connection...
✓ Connected to SQL Server: Microsoft SQL Server...
✓ Database connection successful

2. Creating database tables...
✓ Database tables initialized successfully

✅ Database initialized successfully!

Tables created:
  - registrations
  - otp_verification
  - payments
```

## Step 5: Verify Tables in SSMS

Run this query in SSMS:

```sql
USE webinar_db;
GO

-- List all tables
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE';

-- Check table structures
EXEC sp_help 'registrations';
EXEC sp_help 'otp_verification';
EXEC sp_help 'payments';
```

## Database Schema

### Table: `registrations`
Stores user registration information.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| full_name | NVARCHAR(100) | User's full name |
| email | NVARCHAR(100) | Email (unique) |
| phone | NVARCHAR(20) | Phone number |
| whatsapp_number | NVARCHAR(20) | WhatsApp number |
| city | NVARCHAR(50) | City |
| state | NVARCHAR(50) | State |
| business_name | NVARCHAR(100) | Business name |
| business_type | NVARCHAR(50) | Type of business |
| experience_level | NVARCHAR(50) | Experience level |
| email_verified | BIT | Email verification status |
| payment_status | NVARCHAR(20) | Payment status (pending/success/failed) |
| razorpay_order_id | NVARCHAR(100) | Razorpay order ID |
| razorpay_payment_id | NVARCHAR(100) | Razorpay payment ID |
| amount | DECIMAL(10,2) | Payment amount |
| created_at | DATETIME | Creation timestamp |
| updated_at | DATETIME | Last update timestamp |

### Table: `otp_verification`
Stores OTP codes for email verification.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| email | NVARCHAR(100) | Email address |
| otp | NVARCHAR(6) | 6-digit OTP code |
| expiry | DATETIME | OTP expiry time |
| attempts | INT | Failed verification attempts |
| created_at | DATETIME | Creation timestamp |

### Table: `payments`
Stores payment transaction details.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| registration_id | INT | Foreign key to registrations |
| razorpay_order_id | NVARCHAR(100) | Razorpay order ID |
| razorpay_payment_id | NVARCHAR(100) | Razorpay payment ID |
| razorpay_signature | NVARCHAR(200) | Payment signature |
| amount | DECIMAL(10,2) | Payment amount |
| currency | NVARCHAR(10) | Currency (default: INR) |
| status | NVARCHAR(20) | Payment status |
| payment_method | NVARCHAR(50) | Payment method used |
| created_at | DATETIME | Creation timestamp |

## Troubleshooting

### Error: "Can't open lib 'ODBC Driver 17 for SQL Server'"

**Solution:** Install ODBC Driver 17 for SQL Server
```powershell
# Download and install from:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

Or try using an older driver version in `.env`:
```env
DB_DRIVER=SQL Server
```

### Error: "Login failed for user 'sa'"

**Solutions:**
1. Enable SQL Server authentication in SSMS:
   - Right-click server → Properties → Security → SQL Server and Windows Authentication mode
   - Restart SQL Server service

2. Reset SA password:
   ```sql
   ALTER LOGIN sa WITH PASSWORD = 'NewStrongPassword123!';
   ALTER LOGIN sa ENABLE;
   ```

### Error: "A network-related or instance-specific error"

**Solutions:**
1. Check if SQL Server is running:
   - Open Services (services.msc)
   - Look for "SQL Server (MSSQLSERVER)" or "SQL Server (SQLEXPRESS)"
   - Ensure it's running

2. Enable TCP/IP:
   - Open SQL Server Configuration Manager
   - SQL Server Network Configuration → Protocols
   - Enable TCP/IP
   - Restart SQL Server

3. Check server name:
   ```powershell
   # Find your SQL Server instance name
   Get-Service | Where-Object {$_.DisplayName -like "*SQL Server*"}
   ```

### Error: "Database 'webinar_db' does not exist"

**Solution:** Create the database first in SSMS (see Step 1)

## Testing Connection

Test your database connection:

```powershell
cd backend
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.database import test_connection; test_connection()"
```

## Useful SQL Queries

### View all registrations
```sql
SELECT * FROM registrations ORDER BY created_at DESC;
```

### Count registrations by status
```sql
SELECT payment_status, COUNT(*) as count
FROM registrations
GROUP BY payment_status;
```

### View recent OTPs (for debugging)
```sql
SELECT email, otp, expiry, attempts, created_at
FROM otp_verification
WHERE expiry > GETDATE()
ORDER BY created_at DESC;
```

### View payments
```sql
SELECT p.*, r.full_name, r.email
FROM payments p
JOIN registrations r ON p.registration_id = r.id
ORDER BY p.created_at DESC;
```

### Clean up expired OTPs
```sql
DELETE FROM otp_verification WHERE expiry < GETDATE();
```

## Next Steps

After database setup:

1. **Start backend server:**
   ```powershell
   cd backend
   python run.py
   ```

2. **Check console output** for database connection confirmation

3. **Test OTP flow** - OTPs will now be stored in database instead of memory

4. **View data in SSMS** - Monitor registrations and payments in real-time
