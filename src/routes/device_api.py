from flask import Blueprint, request, jsonify
from src.models.models import db, Device, M3ULink
from datetime import datetime

device_api_bp = Blueprint('device_api', __name__)

@device_api_bp.route('/verify', methods=['POST'])
def verify_device():
    """
    API للتطبيقات للتحقق من MAC Address وإرجاع رابط M3U
    
    Request Body:
    {
        "mac_address": "AA:BB:CC:DD:EE:FF"
    }
    
    Response:
    {
        "status": "active",
        "m3u_url": "http://example.com/playlist.m3u",
        "expiry_date": "2025-12-31",
        "days_left": 365,
        "customer_name": "اسم العميل"
    }
    """
    data = request.get_json()
    
    if not data or 'mac_address' not in data:
        return jsonify({
            'status': 'error',
            'message': 'عنوان MAC مطلوب'
        }), 400
    
    mac_address = data['mac_address'].upper().strip()
    
    # البحث عن الجهاز في قاعدة البيانات
    device = Device.query.filter_by(mac_address=mac_address).first()
    
    if not device:
        return jsonify({
            'status': 'not_found',
            'message': 'الجهاز غير مسجل في النظام',
            'error_code': 'DEVICE_NOT_FOUND'
        }), 404
    
    # التحقق من حالة الجهاز
    if device.status != 'active':
        return jsonify({
            'status': 'inactive',
            'message': 'الجهاز غير نشط. يرجى التواصل مع الموزع',
            'error_code': 'DEVICE_INACTIVE'
        }), 403
    
    # التحقق من تاريخ الانتهاء
    today = datetime.now().date()
    days_left = (device.expiry_date - today).days
    
    if days_left < 0:
        # تحديث حالة الجهاز إلى منتهي
        device.status = 'expired'
        db.session.commit()
        
        return jsonify({
            'status': 'expired',
            'message': 'انتهت صلاحية الاشتراك. يرجى التجديد',
            'expiry_date': device.expiry_date.strftime('%Y-%m-%d'),
            'error_code': 'SUBSCRIPTION_EXPIRED'
        }), 403
    
    # الحصول على رابط M3U النشط
    m3u_link = M3ULink.query.filter_by(status='active').first()
    
    if not m3u_link:
        return jsonify({
            'status': 'error',
            'message': 'لا يوجد رابط M3U متاح حالياً',
            'error_code': 'NO_M3U_AVAILABLE'
        }), 500
    
    # إرجاع البيانات بنجاح
    return jsonify({
        'status': 'active',
        'm3u_url': m3u_link.url,
        'm3u_name': m3u_link.name,
        'expiry_date': device.expiry_date.strftime('%Y-%m-%d'),
        'days_left': days_left,
        'customer_name': device.customer_name,
        'mac_address': device.mac_address,
        'message': 'تم التحقق بنجاح'
    }), 200


@device_api_bp.route('/check/<mac_address>', methods=['GET'])
def check_device_status(mac_address):
    """
    API بسيط للتحقق من حالة الجهاز عبر GET request
    
    مثال: GET /api/device/check/AA:BB:CC:DD:EE:FF
    """
    mac_address = mac_address.upper().strip()
    
    device = Device.query.filter_by(mac_address=mac_address).first()
    
    if not device:
        return jsonify({
            'status': 'not_found',
            'message': 'الجهاز غير مسجل'
        }), 404
    
    today = datetime.now().date()
    days_left = (device.expiry_date - today).days
    
    return jsonify({
        'status': device.status,
        'expiry_date': device.expiry_date.strftime('%Y-%m-%d'),
        'days_left': days_left,
        'customer_name': device.customer_name
    }), 200


@device_api_bp.route('/m3u-links', methods=['GET'])
def get_active_m3u_links():
    """
    API للحصول على جميع روابط M3U النشطة
    """
    m3u_links = M3ULink.query.filter_by(status='active').all()
    
    return jsonify([{
        'id': link.id,
        'name': link.name,
        'url': link.url
    } for link in m3u_links]), 200
