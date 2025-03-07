from flask import request, jsonify, Blueprint
import requests
from app.Container.InstanceContainer import place_schema
from app.Container.InstanceContainer import injector
from app.BLL.Interfaces.IPlaceService import IPlaceService
from app.GUI.model.models import Place, Location
from app.API.Goong.GoongAPI import get_place_detail, get_mutiples_place_detail, get_direction_goong

import asyncio


place_route_bp = Blueprint('place', __name__)

url_openroute_direction = 'https://api.openrouteservice.org/v2/directions/driving-car/geojson'

place_service = injector.get(interface=IPlaceService)


@place_route_bp.route('/api/v1/place/find/<place_id>', methods=['GET'])
async def find_place(place_id):
    place = place_service.get_place(place_id=place_id)
    if (not place):
        data = await get_place_detail(place_id=place_id)
        if ('error' in data):
            return jsonify(data), 400
        location_data = data['location']
        location = Location(latitude=location_data['lat'], longitude=location_data['lng'])
        place = Place(place_id=data['place_id'], formatt_address=data['formatted_address'])
        place = place_service.create_place(place=place, location=location)
        
        if (not place):
            return jsonify(error='Failed when create place'), 400
        
        return place_schema.jsonify(place), 200
    return place_schema.jsonify(obj=place), 200


@place_route_bp.route('/api/v1/place/direction', methods=['POST'])
def find_direction():
    json_data = request.get_json()
    list_pos_null = []
    list_tasks_request = []
    list_create_place = []
    list_data_response_place = []
    coordinates = []
    list_place_id = json_data.get('list_place_id')

    list_places = place_service.get_places_by_list_id_include_null(list_place_id=list_place_id)

    for index, place in enumerate(list_places):
        if (not place):
            list_pos_null.append(index)
            list_tasks_request.append(get_place_detail(list_place_id[index]))

    #Tới đây thì đã có được list_pos_null và list_pos_placeu

    if (len(list_tasks_request) > 0):
        list_data_response_place = asyncio.run(get_mutiples_place_detail(list_corountine=list_tasks_request))
    
    if (list_data_response_place is None):
        return jsonify(error='Error when get multiples place'), 400

    for data in list_data_response_place:
        location = Location(latitude=data['location']['lat'], longitude=data['location']['lng'])
        place = Place(place_id=data['place_id'], formatt_address=data['formatted_address'])
        new_place = place_service.create_place(place=place, location=location)
        
        if (not new_place):
            return jsonify(error='Failed when create place'), 400
        
        list_create_place.append(new_place)
    
    #Tới đây thì đã có list_create_place , list_places

    j = 0
    i = 0
    while (j < len(list_tasks_request)):
        if (i < list_pos_null[j]):
            i+=1
        elif (i == list_pos_null[j]):
            list_places[i] = list_create_place[j]
            i+=1
            j+=1
    

    # for place in list_places:
    #     coord = [place.location.longitude, place.location.latitude]
    #     coordinates.append(coord)

    for place in list_places:
        coord = [place.location.latitude, place.location.longitude]
        coordinates.append(coord)

    
    # coordinates_dict = simplejson.dumps(obj={'coordinates': coordinates}, default=float)

    # pprint.pprint(coordinates_dict)
    # data = asyncio.run(get_direction_ORS(data=coordinates_dict))

    data = asyncio.run(get_direction_goong(coordinates=coordinates))

    if ('error' in data):
        return jsonify(data), 400
    
    return jsonify(data), 200




