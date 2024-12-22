from flask import Blueprint, request, jsonify
from app.GUI.model.models import Location
from app.Container.InstanceContainer import user_location_service, user_service,  location_service, location_schema
from app.custom.Functions import get_coordinate
from flask_jwt_extended import jwt_required, get_jwt_identity

user_location_bp = Blueprint('user_location', __name__)
 


@user_location_bp.route('/api/v1/user/locations', methods=['GET'])
@jwt_required()
def get_user_locations():
    identity = get_jwt_identity()
    user = user_service.get_user_by_id(userid=identity['user_id'])  
    return location_schema.jsonify(user.locations, many=True)



@user_location_bp.route('/api/v1/user/locations', methods=['POST'])
@jwt_required()
def add_user_location():
    lat = lng = location_raw = result = status = None
    json_data = request.get_json()
    address = json_data.get('address')
    if (not address):
        return {'error': 'Vui lòng nhập đầy đủ địa chỉ'}, 400
    identity = get_jwt_identity()
    user = user_service.get_user_by_id(userid=identity['user_id'])    
    check_location, status = location_service.get_location_by_address(location_address=address) #Kiểm tra xem Location có tồn tại trong DB ko
    if (status == 404):
        lat, lng = get_coordinate(query=address) #Nếu không có --> Gửi request để get location
        location_raw = Location(address=address, latitude=lat, longitude=lng)
        result, status = user_location_service.add_location_user(user=user, location=location_raw)
    else:
        if (not any(address == loc.address for loc in user.locations)):
            result, status = user_location_service.add_location_user(user=user, location=check_location)
        else: 
            result, status = check_location, 200

    if (status == 400):
        return jsonify(result), status
    return location_schema.jsonify(result), status
