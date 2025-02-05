from flask import Blueprint, jsonify, request
from app.GUI.model.models import Roles
from app.Container.InstanceContainer import role_schema
from app.Container.InstanceContainer import injector
from app.BLL.Interfaces.IRoleService import IRoleService



role_bp = Blueprint('role', __name__)
role_service = injector.get(interface=IRoleService)

@role_bp.route('/api/v1/roles', methods=['GET'])
def get_roles_all():
    result, status = role_service.get_roles_all()
    return role_schema.jsonify(result, many=True), status


@role_bp.route('/api/v1/roles', methods=['POST'])
def add_role():
    json_data = request.get_json()
    role_name = json_data.get('role_name')
    if (not role_name):
        return {'error': 'Vui lòng điền đủ'}, 400
    if (role_service.check_role(role_name=role_name)):
        return {'error': 'Đã tồn tại ROLE'}, 400    
    role = Roles(role_name=role_name)
    result, status = role_service.add_role(role=role)
    return jsonify(result), status
    


