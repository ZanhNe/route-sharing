from flask import request, jsonify, Blueprint
import requests
from app.extentions.extentions import key_goong
from app.API.Goong.GoongAPI import get_place_detail_goong, get_place_suggest_goong
import asyncio
from app.utils.utils import async_route
find_places_bp = Blueprint('find_places', __name__)



@find_places_bp.route('/api/v1/place/suggest', methods=['POST'])
def handle_suggest_places():
    json_data = request.get_json()
    query = json_data.get('query')
    data = asyncio.run(get_place_suggest_goong(query=query))
    if ('error' in data):
        return jsonify(data), 400
    return jsonify(data), 200
    
@async_route
@find_places_bp.route('/api/v1/place/detail/<place_id>', methods=['GET'])
async def handle_search_places(place_id):
    data = await get_place_detail_goong(place_id=place_id)
    if ('error' in data):
        return jsonify(data), 400
    return jsonify(data)
    
    

