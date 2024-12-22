from flask import Blueprint, jsonify, request
from app.GUI.model.models import User
from app.Container.InstanceContainer import user_service, user_schema
from app.extentions.extentions import bcrypt
from app.BLL.Redis.utils.redis_utils import redis_client

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

