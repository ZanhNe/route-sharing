from firebase_admin import credentials, auth
from firebase_admin.exceptions import FirebaseError
from flask import request, jsonify, Blueprint
from app.BLL.Interfaces.IUserService import IUserService
from app.Container.InstanceContainer import injector, user_schema
from app.GUI.model.models import User

from app.decorator.decorator import middleware_auth

auth_firebase_admin_bp = Blueprint('auth_firebase_admin', __name__)

user_service = injector.get(interface=IUserService)

@auth_firebase_admin_bp.route('/api/v1/admin/users', methods=['GET'])
@middleware_auth
def get_users():
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    user = user_service.get_user_by_id(user_id=decode_token['user_id'])
    if not any(role.role_name == 'ADMIN' for role in user.roles):
        return jsonify(message='Khong co quyen truy cap'), 401
    users = user_service.get_user_all()
    return user_schema.jsonify(obj=users, many=True), 200


@auth_firebase_admin_bp.route('/api/v1/admin/users/<user_id>', methods=['DELETE'])
@middleware_auth
def delete_user(user_id):
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    user = user_service.get_user_by_id(user_id=decode_token['user_id'])
    if not any(role.role_name == 'ADMIN' for role in user.roles):
        return jsonify(message='Khong co quyen truy cap'), 401
    try:
        user_service.delete_user(user_id=user_id)
        auth.delete_user(uid=user_id)
        return jsonify(user_id=user_id, message='Xoa thanh cong'), 200
    except Exception as e:
        return jsonify(message=str(e)), 400
    
@auth_firebase_admin_bp.route('/api/v1/admin/users', methods=['POST'])
@middleware_auth
def create_user():
    from app.tasks.tasks import send_verify_email
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    user = user_service.get_user_by_id(user_id=decode_token['user_id'])
    if not any(role.role_name == 'ADMIN' for role in user.roles):
        return jsonify(message='Khong co quyen truy cap'), 401
    try:
        json_data = request.get_json()
        name = json_data.get('name')
        email = json_data.get('email')
        password = json_data.get('password')
        try:
            user_check = auth.get_user_by_email(email=email)
            raise Exception('Email đã tồn tại với user nào đó, vui lòng kiểm tra lại')
        except auth.UserNotFoundError as e:
            user_firebase = auth.create_user(display_name=name, email=email, email_verified=False, password=password, disabled=False)
            link = auth.generate_email_verification_link(email=email)
            send_verify_email.delay(LINK=link, EMAIL_RECEIVER=email)
            
            user_raw = User(user_id=user_firebase.uid, user_name=name, user_account=email)
            user = user_service.add_user(user=user_raw)
            return user_schema.jsonify(obj=user), 200


        except Exception as e:
            print(e)
            raise e
    
    except ValueError as ve:
        print(ve)
        raise Exception(f'Lỗi {str(ve)}')
    except FirebaseError as fbe:
        print(fbe)
        return 
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400


        


    
