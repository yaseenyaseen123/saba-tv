from flask import Blueprint, request, jsonify
from src.models.models import db, User, Device, M3ULink, Transaction
from werkzeug.security import generate_password_hash
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    total_resellers = User.query.filter_by(role='reseller').count()
    active_devices = Device.query.filter_by(status='active').count()
    total_credits = db.session.query(db.func.sum(User.credits)).filter_by(role='reseller').scalar() or 0
    
    return jsonify({
        'totalResellers': total_resellers,
        'activeDevices': active_devices,
        'totalCredits': total_credits,
        'totalRevenue': 45000
    }), 200

@admin_bp.route('/resellers', methods=['GET'])
def get_resellers():
    resellers = User.query.filter_by(role='reseller').all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'username': r.username,
        'credits': r.credits,
        'devices': Device.query.filter_by(user_id=r.id).count(),
        'status': 'active' if r.credits > 0 else 'inactive'
    } for r in resellers]), 200

@admin_bp.route('/resellers', methods=['POST'])
def create_reseller():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
    
    reseller = User(
        username=data['username'],
        password=generate_password_hash(data['password']),
        name=data['name'],
        role='reseller',
        credits=data.get('credits', 0)
    )
    db.session.add(reseller)
    db.session.commit()
    
    return jsonify({'message': 'تم إضافة الموزع بنجاح', 'id': reseller.id}), 201

@admin_bp.route('/resellers/<int:reseller_id>/credits', methods=['POST'])
def add_credits(reseller_id):
    data = request.get_json()
    amount = data.get('amount', 0)
    
    reseller = User.query.get(reseller_id)
    if not reseller:
        return jsonify({'error': 'الموزع غير موجود'}), 404
    
    reseller.credits += amount
    
    transaction = Transaction(
        user_id=reseller_id,
        type='purchase',
        amount=amount,
        description=f'إضافة {amount} نقطة من المدير'
    )
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'message': 'تم إضافة النقاط بنجاح', 'newCredits': reseller.credits}), 200

@admin_bp.route('/devices', methods=['GET'])
def get_all_devices():
    devices = Device.query.all()
    return jsonify([{
        'id': d.id,
        'mac': d.mac_address,
        'reseller': User.query.get(d.user_id).name,
        'expiryDate': d.expiry_date.strftime('%Y-%m-%d'),
        'status': d.status
    } for d in devices]), 200

@admin_bp.route('/devices', methods=['POST'])
def create_device():
    data = request.get_json()
    
    if Device.query.filter_by(mac_address=data['mac_address']).first():
        return jsonify({'error': 'عنوان MAC موجود بالفعل'}), 400
    
    device = Device(
        mac_address=data['mac_address'],
        customer_name=data['customer_name'],
        user_id=data['user_id'],
        expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(),
        status='active'
    )
    db.session.add(device)
    db.session.commit()
    
    return jsonify({'message': 'تم إضافة الجهاز بنجاح', 'id': device.id}), 201

@admin_bp.route('/m3u', methods=['GET'])
def get_m3u_links():
    links = M3ULink.query.all()
    return jsonify([{
        'id': l.id,
        'name': l.name,
        'url': l.url,
        'devices': l.device_count,
        'status': l.status
    } for l in links]), 200

@admin_bp.route('/m3u', methods=['POST'])
def create_m3u_link():
    data = request.get_json()
    
    link = M3ULink(
        name=data['name'],
        url=data['url'],
        status='active',
        device_count=0
    )
    db.session.add(link)
    db.session.commit()
    
    return jsonify({'message': 'تم إضافة الرابط بنجاح', 'id': link.id}), 201
