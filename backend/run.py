from app import create_app
import os

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    PORT = app.config['PORT']
    DEBUG = app.config['DEBUG']
    
    print(f'Server running at http://localhost:{PORT}')
    print('Razorpay integration ready!')
    
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
