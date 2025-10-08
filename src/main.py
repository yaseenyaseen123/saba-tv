import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.models import db, User, Device, M3ULink, Transaction
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from src.routes.reseller import reseller_bp
from src.routes.device_api import device_api_bp
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'saba_tv_secret_key_2025'

# Enable CORS for all origins
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Register blueprints FIRST - this is critical!
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(reseller_bp, url_prefix='/api/reseller')
app.register_blueprint(device_api_bp, url_prefix='/api/device')

# Database configuration
# Use PostgreSQL if DATABASE_URL is set (Railway), otherwise use SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Railway provides postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Fallback to SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database
with app.app_context():
    try:
        # Ensure database directory exists
        db_path = os.path.join(os.path.dirname(__file__), 'database')
        os.makedirs(db_path, exist_ok=True)
        
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Check if admin user exists, if not create one
        if not User.query.filter_by(username='admin').first():
            # Create default admin user
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                name='المدير الرئيسي',
                role='admin',
                credits=0
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully")
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

# Serve index.html for root
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files - this will only match if no API route matched
@app.route('/<path:filename>')
def serve_static(filename):
    # Check if it's a static file that exists
    file_path = os.path.join(app.static_folder, filename)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, filename)
    # Otherwise, serve index.html for client-side routing (SPA)
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
