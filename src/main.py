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
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'saba_tv_secret_key_2025'

# Enable CORS for development
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(reseller_bp, url_prefix='/api/reseller')

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
    db.create_all()
    
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
        print("✅ Database initialized with admin user")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
