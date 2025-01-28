# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
# from app.Container.InstanceContainer import user_service, place_service, route_place_service, route_share_service, route_share_schema, user_schema, request_route_service, notification_service, request_route_schema, notification_schema, match_route_schema, match_route_service
# from app.GUI.model.models import UserRouteShare, Status, RequestRoute, Notification, NotificationType, MatchRoute
# from app.BLL.Redis.utils.redis_utils import redis_client
# import simplejson



# route_share_bp = Blueprint('route_share_bp', __name__)

# @route_share_bp.route('/api/v1/user/share', methods=['POST'])
# @jwt_required()
# def handle_share_route():
    
#     flag = False
#     json_data = request.get_json()
#     identity = get_jwt_identity() #Lấy identity từ Token hiện tại
#     for role in identity['roles']:
#         if (role == 'USER'):
#             flag = True
#             break
    
#     if (not flag):
#         return jsonify(statusText='You do not have permisson'), 401
    
#     first_location = json_data.get('firstLocation')
#     second_location = json_data.get('secondLocation')

#     share_name = json_data.get('share_name')
#     share_description = json_data.get('share_description')

#     user = user_service.get_user_by_id(user_id=identity['user_id'])
#     route = route_place_service.get_route_with_place(route_name='', list_place_id=[first_location['place_id'], second_location['place_id']])
#     route_share = UserRouteShare(share_name=share_name, share_description=share_description)
#     route_share_after_solve = route_share_service.add_route_share(route_share=route_share, user=user, route=route)

#     if (not route_share_after_solve):
#         return jsonify(statusText='Failed when create route share'), 400
    
#     list_routes_share_json = route_share_schema.dump(route_share_service.get_all_routes_share_is_not_match(), many=True)
#     data_json_str = simplejson.dumps({'payload': list_routes_share_json})
    
#     user_after = user_service.update_status_user(new_status=Status.WAITING, user=user)
#     user_json = user_schema.dump(obj=user_after)

#     data_user_json_str = simplejson.dumps({'payload': user_json, 'send_to': user.user_id})
    


#     redis_client.publish('routes_share.update', data_json_str)
#     redis_client.publish('user.update', data_user_json_str)


#     # user_after_json = user_schema.dump(obj=user_after)
#     # route_share_after_solve_json = route_share_schema.dump(obj=route_share_after_solve)

#     # return jsonify(route_share=route_share_after_solve_json), 200
#     return jsonify(status='success', message='Share route successful'), 200


# @route_share_bp.route('/api/v1/user/share', methods=['GET'])
# def get_list_share():
#     list_routes_share = route_share_service.get_all_routes_share_is_not_match()
#     return route_share_schema.jsonify(obj=list_routes_share, many=True), 200

# @route_share_bp.route('/api/v1/user/request', methods=['POST'])
# @jwt_required()
# def handle_request_match():
#     json_data = request.get_json()

#     secondary_user_id = get_jwt_identity()['user_id']
#     main_user_id = json_data.get('main_user_id')
#     list_place_id = json_data.get('list_place_id')


#     secondary_user = user_service.get_user_by_id(user_id=secondary_user_id)
#     main_user = user_service.get_user_by_id(user_id=main_user_id)
#     route = route_place_service.get_route_with_place(route_name='', list_place_id=list_place_id)


#     request_route_service.create_request_route(main_user=main_user, secondary_user=secondary_user, route=route)
#     notification_service.add_new_notification_of_user(noti_type=NotificationType.REQUEST, content=f'{secondary_user.user_name} vừa gửi yêu cầu ghép route', main_user=main_user, secondary_user=secondary_user)

#     requests_route = request_route_service.get_requests_route_main_user_pending(main_user_id=main_user_id)
#     notifications = notification_service.get_all_notifications_of_user(user_id=main_user_id)

#     requests_route_json = request_route_schema.dump(obj=requests_route, many=True)
#     notifications_request_json = notification_schema.dump(obj=notifications, many=True)

#     data_requests_json_str = simplejson.dumps({'payload': requests_route_json, 'send_to': main_user_id})
#     data_noti_json_str = simplejson.dumps({'payload': notifications_request_json, 'send_to': main_user_id})

#     secondary_user_after = user_service.update_status_user(new_status=Status.WAITING, user=secondary_user)
#     secondary_user_after_json = user_schema.dump(obj=secondary_user_after)

#     data_secondary_user_json_str = simplejson.dumps({'payload': secondary_user_after_json, 'send_to': secondary_user_id})

#     redis_client.publish('notification.update', data_noti_json_str)
#     redis_client.publish('request_route.update', data_requests_json_str)
#     redis_client.publish('user.update', data_secondary_user_json_str)
    

#     return jsonify(status='success', message='Send request successful'), 200

# @route_share_bp.route('/api/v1/user/request/<int:request_id>/accept', methods=['GET'])
# @jwt_required()
# def handle_request_accept(request_id):
#     main_user_id = get_jwt_identity()['user_id']
#     list_user_id = []
#     list_user_id.append()
#     list_request_route_before = request_route_service.get_requests_route_main_user_pending(main_user_id=main_user_id)
#     request_accepted = request_route_service.get_request_by_request_id(request_id=request_id)

#     for request_before in list_request_route_before:
#         if (request_before.request_id != request_id):
#             list_user_id.append(request_before.secondary_user.user_id)

#     main_user = request_accepted.main_user
#     secondary_user = request_accepted.secondary_user
#     route = request_accepted.route

#     list_user_after_update_status = user_service.update_status_user_request(main_user_id_accept=main_user_id, secondary_user_id_accept=secondary_user.user_id, list_declined_user_id=list_user_id)
#     main_user_after = user_schema.get_user_by_id(user_id=main_user_id)
#     main_user_after_json = user_schema.dump(obj=main_user_after)
#     main_user_after_json_str = simplejson.dumps({'payload': main_user_after_json, 'send_to': main_user_id})
    

#     request_route_service.update_status_accept_request(main_user_id=main_user_id, request_id=request_id)

#     list_request_id = [req.request_id for req in list_request_route_before]

#     list_request_route_after = request_route_service.get_requests_by_list_request_id(list_request_id=list_request_id)

#     list_request_route_after_json = request_route_schema.dump(obj=list_request_route_after, many=True)

#     data_requests_json_str = simplejson.dumps({'payload': list_request_route_after_json, 'send_to': main_user_id})

#     redis_client.publish('request_route.update', data_requests_json_str)
#     redis_client.publish('user.update', main_user_after_json_str)

#     for request_route, user in zip(list_request_route_after, list_user_after_update_status):
#         request_route_json = request_route_schema.dump(obj=request_route)
#         request_route_json_str = simplejson.dumps({'payload': request_route_json, 'send_to': request_route.secondary_user.user_id})

#         user_json = user_schema.dump(obj=user)
#         user_json_str = simplejson.dumps({'payload': user_json, 'send_to': user.user_id})

#         redis_client.publish('request_route.update', request_route_json_str)
#         redis_client.publish('user.update', user_json_str)
#     #sửa lại status của các user bị declined --> free : DONE 
#     #Tạo match route giữa 2 user : DONE
#     #sửa lại status của main_user và secondary_user : Matching : DONE
#     match_route = match_route_service.create_new_match(main_user=main_user, secondary_user=secondary_user, route=route)


#     return jsonify(message='Success'), 200






    
