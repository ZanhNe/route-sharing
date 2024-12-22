from flask import request, jsonify, Blueprint
import requests
from app.extentions.extentions import key_goong
from app.API.Goong.GoongAPI import get_place_detail_goong, get_place_suggest_goong
import asyncio
from app.utils.utils import async_route
find_places_bp = Blueprint('find_places', __name__)



# def run_coroutine(coroutine):
#     try:
#         # Kiểm tra xem có event loop nào đang chạy không :v
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         # Không có loop nào đang chạy, tạo một loop mới
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
    
#     # Chạy coroutine trên event loop hiện tại
#     return loop.run_until_complete(coroutine)

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
    # data = asyncio.run(get_place_detail_goong(place_id=place_id))
    data = await get_place_detail_goong(place_id=place_id)
    if ('error' in data):
        return jsonify(data), 400
    return jsonify(data)
    
    

