"""
Database connection and operations for SQL Server
"""
import pyodbc
from flask import current_app, g
from contextlib import contextmanager

def get_db_connection():
    """Create and return a database connection"""
    config = current_app.config
    
    connection_string = (
        f"DRIVER={{{config['DB_DRIVER']}}};"
        f"SERVER={config['DB_SERVER']};"
        f"DATABASE={config['DB_NAME']};"
        f"UID={config['DB_USER']};"
        f"PWD={config['DB_PASSWORD']};"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        raise

@contextmanager
def get_db_cursor():
    """Context manager for database operations"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Database operation error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db_cursor() as cursor:
        # Create registrations table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='registrations' AND xtype='U')
            CREATE TABLE registrations (
                id INT IDENTITY(1,1) PRIMARY KEY,
                full_name NVARCHAR(100) NOT NULL,
                email NVARCHAR(100) NOT NULL UNIQUE,
                phone NVARCHAR(20) NOT NULL,
                whatsapp_number NVARCHAR(20),
                city NVARCHAR(50),
                state NVARCHAR(50),
                business_name NVARCHAR(100),
                business_type NVARCHAR(50),
                experience_level NVARCHAR(50),
                email_verified BIT DEFAULT 0,
                payment_status NVARCHAR(20) DEFAULT 'pending',
                razorpay_order_id NVARCHAR(100),
                razorpay_payment_id NVARCHAR(100),
                amount DECIMAL(10,2),
                created_at DATETIME DEFAULT GETDATE(),
                updated_at DATETIME DEFAULT GETDATE()
            )
        """)
        
        # Create OTP table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='otp_verification' AND xtype='U')
            CREATE TABLE otp_verification (
                id INT IDENTITY(1,1) PRIMARY KEY,
                email NVARCHAR(100) NOT NULL,
                otp NVARCHAR(6) NOT NULL,
                expiry DATETIME NOT NULL,
                attempts INT DEFAULT 0,
                created_at DATETIME DEFAULT GETDATE(),
                INDEX idx_email (email),
                INDEX idx_expiry (expiry)
            )
        """)
        
        # Create payments table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='payments' AND xtype='U')
            CREATE TABLE payments (
                id INT IDENTITY(1,1) PRIMARY KEY,
                registration_id INT,
                razorpay_order_id NVARCHAR(100),
                razorpay_payment_id NVARCHAR(100),
                razorpay_signature NVARCHAR(200),
                amount DECIMAL(10,2),
                currency NVARCHAR(10) DEFAULT 'INR',
                status NVARCHAR(20),
                payment_method NVARCHAR(50),
                created_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (registration_id) REFERENCES registrations(id)
            )
        """)
        
        print("✓ Database tables initialized successfully")

def test_connection():
    """Test database connection"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()
            print(f"✓ Connected to SQL Server: {version[0][:50]}...")
            return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
