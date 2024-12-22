from flask import Blueprint, jsonify, request
from app.GUI.model.models import Route
from app.Container.InstanceContainer import route_service, route_schema

route_bp = Blueprint('route', __name__)

@route_bp.route('/api/v1/routes', methods=['GET'])
def get_routes_all():
    result, status = route_service.get_routes_all()
    return route_schema.jsonify(result, many=True), status

@route_bp.route('/api/v1/routes', methods=['POST'])
def add_route():
    pass

@route_bp.route('/api/v1/routes/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    json_data = request.get_json()
    route_name = json_data.get('route_name')
    if (not route_name):
        return jsonify({'error': 'Vui lòng điền tên tuyến đường để sửa'}), 400
    result_get_route, status = route_service.get_route(route_id=route_id)
    if (status == 404):
        return jsonify(result_get_route), status
    new_route = Route(route_name=route_name)
    result_updated_route, status = route_service.update_route(route=result_get_route, new_route=new_route)

    if (status == 400):
        return jsonify(result_updated_route), status
    return route_schema.jsonify(result_updated_route), status
    


@route_bp.route('/api/v1/routes', methods=['DELETE'])
def delete_all_routes():
    pass

@route_bp.route('/api/v1/routes/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    route = route_service.get_route(route_id=route_id)
    result, status = route_service.delete_route(route=route)
    if (status == 400):
        return jsonify(result), status
    return jsonify(result), status