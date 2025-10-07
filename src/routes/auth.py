from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from src.models.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'role': user.role,
            'credits': user.credits
        }
    }), 200
