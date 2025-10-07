from flask import Blueprint, request, jsonify
from src.models.models import db, User, Device, Transaction
from datetime import datetime, timedelta

reseller_bp = Blueprint('reseller', __name__)

@reseller_bp.route('/<int:user_id>/devices', methods=['GET'])
def get_devices(user_id):
    devices = Device.query.filter_by(user_id=user_id).all()
    
    result = []
    for d in devices:
        days_left = (d.expiry_date - datetime.now().date()).days
        result.append({
            'id': d.id,
            'mac': d.mac_address,
            'customerName': d.customer_name,
            'expiryDate': d.expiry_date.strftime('%Y-%m-%d'),
            'status': d.status,
            'daysLeft': days_left
        })
    
    return jsonify(result), 200

@reseller_bp.route('/<int:user_id>/devices', methods=['POST'])
def create_device(user_id):
    data = request.get_json()
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'المستخدم غير موجود'}), 404
    
    if user.credits < 50:
        return jsonify({'error': 'رصيدك غير كافٍ'}), 400
    
    if Device.query.filter_by(mac_address=data['mac_address']).first():
        return jsonify({'error': 'عنوان MAC موجود بالفعل'}), 400
    
    device = Device(
        mac_address=data['mac_address'],
        customer_name=data['customer_name'],
        m3u_url=data.get('m3u_url', ''),  # رابط M3U8 خاص بالجهاز
        user_id=user_id,
        expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(),
        status='active'
    )
    
    user.credits -= 50
    
    transaction = Transaction(
        user_id=user_id,
        type='usage',
        amount=-50,
        description='تفعيل جهاز جديد'
    )
    
    db.session.add(device)
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'تم إضافة الجهاز بنجاح',
        'id': device.id,
        'newCredits': user.credits
    }), 201

@reseller_bp.route('/<int:user_id>/transactions', methods=['GET'])
def get_transactions(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    
    return jsonify([{
        'id': t.id,
        'type': t.type,
        'amount': t.amount,
        'description': t.description,
        'date': t.created_at.strftime('%Y-%m-%d')
    } for t in transactions]), 200

@reseller_bp.route('/<int:user_id>/stats', methods=['GET'])
def get_stats(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        devices = Device.query.filter_by(user_id=user_id).all()
        total_devices = len(devices)
        active_devices = len([d for d in devices if d.status == 'active'])
        
        expiring_devices = 0
        for d in devices:
            days_left = (d.expiry_date - datetime.now().date()).days
            if 0 < days_left <= 30:
                expiring_devices += 1
        
        return jsonify({
            'credits': user.credits,
            'totalDevices': total_devices,
            'activeDevices': active_devices,
            'expiringDevices': expiring_devices
        }), 200
    except Exception as e:
        print(f"Error in get_stats: {e}")
        return jsonify({'error': str(e)}), 500
