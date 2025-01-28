from flask import Blueprint, jsonify, request
from app.GUI.model.models import User
from app.Container.InstanceContainer import user_service, user_schema
from app.extentions.extentions import bcrypt
from app.BLL.Redis.utils.redis_utils import redis_client
from firebase_admin import auth
from datetime import datetime
from app.utils.utils import Helper
from app.decorator.decorator import middleware_auth
import cloudinary.uploader
user_bp = Blueprint('user', __name__)

@user_bp.route('/api/v1/users', methods=['GET'])
def get_user_all():
    result, status = user_service.get_user_all()
    return user_schema.jsonify(result, many=True), status

@user_bp.route('/api/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_json = redis_client.json().get(f'user_{user_id}', '$')
    if (not user_json):
        user = user_service.get_user_by_id(user_id=user_id)
        if (not user):
            return jsonify(error='User not found'), 404
        return user_schema.jsonify(obj=user), 200
    return jsonify(user_json), 200
    
@user_bp.route('/api/v1/users/sync', methods=['POST'])
@middleware_auth
def sync_user():
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token, clock_skew_seconds=10)
    uid = decode_token['user_id']
    json_data = request.get_json()
    user = user_service.get_user_by_id(user_id=uid)
    if (not user):
        uid = json_data.get('uid')
        displayName = json_data.get('displayName')
        email = json_data.get('email')
        photoURL = json_data.get('photoURL')
        phoneNumber = json_data.get('phoneNumber')
        createdAt = json_data.get('createdAt')
        updatedAt = json_data.get('updatedAt')        
        created_at_ts = Helper.convert_datetime_iso(datetime_str=createdAt)
        updated_at_ts = Helper.convert_datetime_iso(datetime_str=updatedAt) if updatedAt != None else None
        user = User(user_id=uid, user_name=displayName, user_account=email, avatar=photoURL, phone=phoneNumber, created_time=created_at_ts, updated_time=updated_at_ts)
        user = user_service.add_user(user=user)
        if (not user):
            return jsonify(error='Error when create new user'), 401

    return user_schema.jsonify(obj=user), 200
    
    


@user_bp.route('/api/v1/user', methods=['POST'])
def register_user():
    json_data = request.get_json()
    username = json_data.get('user_name')
    useraccount = json_data.get('user_account')
    unhashpass = json_data.get('password')
    if (not username or not useraccount or not unhashpass):
       return {'error': 'Vui lòng điền đủ thông tin'}, 400
    hash_pass = bcrypt.generate_password_hash(unhashpass)
    new_user = User(user_name=username, user_account=useraccount, password=hash_pass)
    user = user_service.add_user(user=new_user)
    if (not user):
        return jsonify(error='Error when add user'), 400
    return user_schema.jsonify(user), 200


@user_bp.route('/api/v1/user/upload', methods=['POST'])
@middleware_auth
def update_user():
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    uid = decode_token['user_id']
    user = user_service.get_user_by_id(user_id=uid)

    phone = request.form['phone']
    full_name = request.form['fullName']

    if (not user): 
        return jsonify(status='User không tồn tại'), 404

    if 'avatar' in request.files:
        file = request.files['avatar']
        try:
            result = cloudinary.uploader.upload(file=file, folder='avatar', use_filename=True)
            user.avatar = result['secure_url']
            user.user_name = full_name
            user.phone = phone
            user.updated_time = datetime.now()
            user_after = user_service.update_user(user=user)
            if (not user_after):
                return jsonify(status='FAILED', message='Error when update user'), 400
            return user_schema.jsonify(obj=user_after), 200
        except Exception as e:
            print(e)
            return jsonify(error='error')
    else: 
        return jsonify(status='KO NHAN DUOC FILE'), 400
    