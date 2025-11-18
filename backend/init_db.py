"""
Database initialization script
Run this to create database tables
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database import init_db, test_connection

if __name__ == '__main__':
    print('=== Database Initialization ===\n')
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        print('1. Testing database connection...')
        if not test_connection():
            print('\n❌ Database connection failed!')
            print('\nPlease check your .env file and ensure:')
            print('  - DB_SERVER is correct (e.g., localhost or server name)')
            print('  - DB_NAME exists')
            print('  - DB_USER and DB_PASSWORD are correct')
            print('  - SQL Server is running')
            print('  - ODBC Driver 17 for SQL Server is installed')
            sys.exit(1)
        
        print('\n2. Creating database tables...')
        try:
            init_db()
            print('\n✅ Database initialized successfully!')
            print('\nTables created:')
            print('  - registrations')
            print('  - otp_verification')
            print('  - payments')
        except Exception as e:
            print(f'\n❌ Failed to initialize database: {e}')
            sys.exit(1)
