"""
Script to create settings table in database
"""
from app import create_app
from app.database import get_db_cursor

def create_settings_table():
    app = create_app()
    with app.app_context():
        with get_db_cursor() as cursor:
            # Create settings table if it doesn't exist
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'settings')
            CREATE TABLE settings (
                id INT IDENTITY(1,1) PRIMARY KEY,
                setting_key NVARCHAR(100) UNIQUE NOT NULL,
                value NVARCHAR(MAX) NOT NULL,
                created_at DATETIME DEFAULT GETDATE(),
                updated_at DATETIME DEFAULT GETDATE()
                )
            """)
            print('✓ Settings table created successfully')
            
            # Insert default webinar settings if not exist
            cursor.execute("SELECT COUNT(*) FROM settings WHERE setting_key = 'webinar_date'")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO settings (setting_key, value) VALUES 
                    ('webinar_date', 'December 10, 2025'),
                    ('webinar_time', '9:00 AM - 12:00 PM IST'),
                    ('webinar_title', 'The Needles Webinar'),
                    ('zoom_link', '')
                """)
                print('✓ Default webinar settings inserted')
            else:
                print('✓ Settings already exist')

if __name__ == '__main__':
    create_settings_table()
