import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///itraveda.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Razorpay test keys (replace with your actual ones in production)
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'rzp_test_xxxxxx'
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'your_secret_key'

    # Email settings (for order confirmations etc.)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your_email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your_email_password'

    # OTP / SMS (optional)
    SMS_API_KEY = os.environ.get('SMS_API_KEY') or 'your_fast2sms_api_key'
    
