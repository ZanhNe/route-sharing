# from flask import Blueprint, jsonify, request
# from app.GUI.model.models import User, Route
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.Container.InstanceContainer import route_place_service, user_route_service, user_service, route_schema


# user_route_bp = Blueprint('user_route', __name__)

# @user_route_bp.route('/api/v1/user/routes', methods=['GET'])
# def get_user_routes():
#     pass

# @user_route_bp.route('/api/v1/user/routes', methods=['POST'])
# @jwt_required()
# def add_route_to_user():
#     result_user_route = status_user_route = None
#     json_data = request.get_json()
#     first_location_address = json_data.get('first_location_address')
#     second_location_address = json_data.get('second_location_address')
#     route_name = second_location_address
#     if (not first_location_address or not second_location_address):
#         return {'error': 'Vui lòng điền đủ thông tin 2 tọa độ'}, 401
#     result_location_route, status_location_route = route_location_service.get_route_with_location(
#         route_name=route_name, 
#         first_location_address=first_location_address, 
#         second_location_address=second_location_address) #get ra route với 2 địa chỉ location được gửi từ request

#     if (status_location_route == 401):
#         return jsonify(result_location_route), status_location_route 
#     identity = get_jwt_identity() #Lấy identity từ Token hiện tại
#     user = user_service.get_user_by_id(userid=identity['user_id']) #Từ identity đó --> get ra user đang hoạt động
#     if (not any(result_location_route.route_id == route.route_id for route in user.routes)): #Nếu user chưa tồn tại route -> add Route vào user
#         result_user_route, status_user_route = user_route_service.add_route_to_user(user=user, route=result_location_route)
#     else: 
#         result_user_route, status_user_route = user, 200
#     if (status_user_route == 401):
#         return jsonify(result_user_route), status_user_route

#     return route_schema.jsonify(result_location_route), status_location_route
    
    

