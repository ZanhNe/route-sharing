from flask import Blueprint, request, jsonify
from app.extentions.extentions import bcrypt, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from app.Container.InstanceContainer import user_service, user_schema
from app.BLL.Redis.utils.redis_utils import redis_client
import simplejson

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/v1/auth/login', methods=['POST']) 
def login():
    json_data = request.get_json()
    user_name = json_data.get('user_name')
    password = json_data.get('password')
    user, status = user_service.get_user_by_account(user_account=user_name)
    if (status == 404):
        return jsonify({'error': 'Không tồn tại account', 'status': status})

    #So sanh hash_pass va pass tu user
    if (not bcrypt.check_password_hash(pw_hash=user.password, password=password)):
        return jsonify({'error': 'Sai mật khẩu', 'status': 404})
    access_token = create_access_token(identity=user, fresh=True)
    refresh_token = create_refresh_token(identity=user)
    user_json = user_schema.dump(obj=user)

    redis_client.json().set(f'user_{user.user_id}', '$', user_json)
    users = simplejson.loads(redis_client.get('users'))
    users.append(user_json)
    redis_client.set('users', simplejson.dumps(obj=users))

    return jsonify(user=user_json, access_token=access_token, refresh_token=refresh_token, status=200), 200



# @auth_bp.route('/api/v1/auth/register', methods=['POST']) 
# def signup():
#     return {'success': 'Test', 'status': 200}, 200

#Token Freshness pattern
@auth_bp.route('/api/v1/auth/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=new_access_token)



    



