from flask import Blueprint, request
from app.GUI.model.models import Location
from app.Container.InstanceContainer import location_service, location_schema
from app.extentions.extentions import geocoder


location_bp = Blueprint('location', __name__)
def get_coordinate(query: str):
    results = geocoder.geocode(query=query)
    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    return lat, lng    

@location_bp.route('/api/v1/locations', methods=['GET'])
def get_locations_all():
    result, status = location_service.get_locations_all()
    if (status == 200):
        return location_schema.jsonify(result, many=True)



@location_bp.route('/api/v1/locations', methods=['POST'])
def add_location():
    json_data = request.get_json()
    address = json_data.get('address')
    if (not address):
        return {'error': 'Vui lòng nhập địa chỉ'}, 400
    lat, lng = get_coordinate(query=address)
    location_raw = Location(address=address, latitude=lat, longitude=lng)
    location = location_service.add_location(location=location_raw)
    return location_schema.jsonify(location), 200


