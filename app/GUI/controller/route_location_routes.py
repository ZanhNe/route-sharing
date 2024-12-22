# from flask import Blueprint, request, jsonify
# import simplejson as json
# from app.custom.Functions import get_coordinate, get_direction
# from app.GUI.model.models import Location
# from app.Container.InstanceContainer import location_service, location_schema, route_location_service
# from app.custom.Functions import get_coordinate
# from flask_jwt_extended import jwt_required, get_jwt_identity

# route_location_bp = Blueprint('route_location', __name__)

# def handle_location(location_address: str):
#     location, status_location = location_service.get_location_by_address(location_address=location_address)
#     if (status_location == 404):
#         lat, lng = get_coordinate(query=location_address)
#         location = Location(address=location_address, latitude=lat, longitude=lng)
#         location, status_add_location = location_service.add_location(location=location)
#         return location, status_add_location
#     return location, status_location

# @route_location_bp.route('/api/v1/route/<int:route_id>/locations', methods=['GET'])
# def get_route_locations(route_id):
#     pass

# @route_location_bp.route('/api/v1/route/<int:route_id>/locations', methods=['POST'])
# def add_route_locations(route_id):
#     pass

# @route_location_bp.route('/api/v1/route/locations', methods=['POST'])
# # @jwt_required()
# def get_direction_routing():
#     json_data = request.get_json()
#     first_location_address = json_data.get('first_location_address')
#     second_location_address = json_data.get('second_location_address')
#     if (not first_location_address or not second_location_address):
#         return {'error': 'Vui lòng nhập đủ thông tin 2 địa chỉ'}, 400
#     first_location, status_first_location = handle_location(location_address=first_location_address)
#     second_location, status_second_location = handle_location(location_address=second_location_address)

#     if (status_first_location == 400):
#         return jsonify(first_location), status_first_location
#     if (status_second_location == 400):
#         return jsonify(second_location), status_second_location
    
#     route = get_direction(first_location=first_location, second_location=second_location)
    
#     if (not route):
#         return jsonify({'error': 'Lỗi khi get direction'}), 400
#     return jsonify(route), 200
    
    



