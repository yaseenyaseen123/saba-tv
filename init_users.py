#!/usr/bin/env python3.11
"""
Script to initialize default users in the database
"""
import sys
sys.path.insert(0, '/home/ubuntu/saba-tv-production')

from src.main import app
from src.models.models import db, User
from werkzeug.security import generate_password_hash

def init_users():
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                name='المدير الرئيسي',
                role='admin',
                credits=0
            )
            db.session.add(admin)
            print("✅ تم إنشاء حساب المدير")
        else:
            print("ℹ️  حساب المدير موجود بالفعل")
        
        # Check if test reseller exists
        reseller = User.query.filter_by(username='test123').first()
        if not reseller:
            reseller = User(
                username='test123',
                password=generate_password_hash('test123'),
                name='موزع تجريبي',
                role='reseller',
                credits=100
            )
            db.session.add(reseller)
            print("✅ تم إنشاء حساب الموزع التجريبي")
        else:
            print("ℹ️  حساب الموزع التجريبي موجود بالفعل")
        
        db.session.commit()
        print("\n🎉 تم إنشاء المستخدمين بنجاح!")
        print("\nبيانات الدخول:")
        print("المدير: admin / admin123")
        print("الموزع: test123 / test123 (100 نقطة)")

if __name__ == '__main__':
    init_users()
