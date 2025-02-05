# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.GUI.model.models import User, Roles
# from app.Container.InstanceContainer import user_role_service, role_service, user_service



# user_role_bp = Blueprint('user_role', __name__)

# @user_role_bp.route('/api/v1/user/roles', methods=['GET'])
# def get_user_roles():
#     pass

# @user_role_bp.route('/api/v1/user/roles', methods=['POST'])
# @jwt_required()
# def add_role_user():
#     role_list = []
#     json_data = request.get_json()
#     if (not bool(json_data)):
#         return {'error': 'Không có thông tin'}, 400
#     role_list_request = json_data.get('roles')
#     if (not len(role_list_request)):
#         return jsonify({'error': 'Vui lòng thêm ít nhất 1 Role'}), 400
#     for role_name in role_list_request:
#         role_list.append(role_name.upper())
    
#     print(role_list) #test in ra coi thử
#     roles = role_service.get_list_role(roles=role_list)

#     identity = get_jwt_identity()
#     user = user_service.get_user_by_id(userid=identity['user_id'])

#     result, status = user_role_service.add_role_user(user=user, roles=roles)
#     if (status == 400):
#         return jsonify(result), status
#     return jsonify({'success': 'Đã thêm thành công Role cho User'}), status


