from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.Container.InstanceContainer import \
                                     schedule_management_schema, schedule_share_item_schema\
                                    , roadmap_share_schema, create_roadmap_request_validator\
                                    , roadmap_request_schema, notification_schema, update_schedule_management_schema\
                                    , update_schedule_share_schema   

from app.BLL.Interfaces.IScheduleManagementShareRoute import IScheduleManagementShareRoute   
from app.BLL.Interfaces.IScheduleManagementService import IScheduleManagementService
from app.BLL.Interfaces.IRoadmapShareService import IRoadmapShareService
from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.Container.InstanceContainer import injector     
from app.BLL.Redis.utils.redis_utils import redis_client
from app.decorator.decorator import middleware_auth
from firebase_admin import auth
import simplejson



schedule_management_bp = Blueprint('schedule_management', __name__)

schedule_management_share_route = injector.get(interface=IScheduleManagementShareRoute)
schedule_management_service = injector.get(interface=IScheduleManagementService)
roadmap_share_service = injector.get(interface=IRoadmapShareService)
roadmap_request_service = injector.get(interface=IRoadmapRequestService)



@schedule_management_bp.route('/api/v1/schedule-managements/users/<user_id>', methods=['GET'])
def get_all_schedule_managements_of_user(user_id):
    schedule_managements = schedule_management_service.get_all_schedule_management_by_user_id(user_id=user_id)
    return schedule_management_schema.jsonify(obj=schedule_managements, many=True), 200

@schedule_management_bp.route('/api/v1/schedule-managements/<schedule_management_title>/users/<user_id>', methods=['GET'])
@middleware_auth
def get_schedule_management_of_user_by_title(schedule_management_title, user_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id_token = decode_token['user_id']
        if user_id_token != user_id:
            raise Exception('Không có quyền truy cập vào tài nguyên')
        schedule_managements = schedule_management_service.get_schedule_management_by_title_and_user_id(schedule_management_title=schedule_management_title, user_id=user_id)
        return schedule_management_schema.jsonify(obj=schedule_managements, many=True), 200
    except Exception as e:
        return jsonify(message=str(e)), 401

@schedule_management_bp.route('/api/v1/schedule-managements/<int:schedule_management_id>', methods=['GET'])
@middleware_auth
def get_schedule_management_of_user(schedule_management_id):
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    schedule_management = schedule_management_service.get_schedule_management_by_schedule_management_id(schedule_management_id=schedule_management_id)
    if (not schedule_management.is_open and schedule_management.user.user_id != decode_token['user_id']):
        return jsonify(message='Không được phép truy cập danh sách đã đóng'), 403
    return schedule_management_schema.jsonify(obj=schedule_management), 200

@schedule_management_bp.route('/api/v1/schedule-managements/users/<user_id>', methods=['POST'])
@middleware_auth
def create_schedule_management_for_user(user_id):
    json_data = request.get_json()
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    try:
        if (user_id != decode_token['user_id']):
            raise Exception('Không được phép thao tác tài nguyên của user khác')
        scheduleManagementMapper = schedule_management_schema.load(data=json_data)
        scheduleManagementMapper.user_id = user_id
        scheduleManagementCreate = schedule_management_service.create_schedule_management(schedule_management=scheduleManagementMapper)
        scheduleManagementCreateJson = schedule_management_schema.dump(obj=scheduleManagementCreate)
        dataObjectPayload = simplejson.dumps({'payload': scheduleManagementCreateJson})
        # print(dataObjectPayload)
        redis_client.publish('schedule_managements.update', message=dataObjectPayload)
        return schedule_management_schema.jsonify(obj=scheduleManagementCreate), 201
    except ValidationError as ve:
        print(ve.messages)
        return jsonify({"errors": ve.messages['content']}), 422
    except SQLAlchemyError as sae:
        return jsonify({"errors": str(sae)}), 500
    except Exception as ex:
        return jsonify({"errors": str(ex)}), 401

@schedule_management_bp.route('/api/v1/schedule-managements/is-open', methods=['GET'])
def get_all_schedule_managements_opening():
    schedule_managements = schedule_management_service.get_all_schedule_managements_opening()
    return schedule_management_schema.jsonify(obj=schedule_managements, many=True), 200

@schedule_management_bp.route('/api/v1/schedule-managements/<int:schedule_management_id>', methods=['PUT'])
@middleware_auth
def set_open_status_schedule_management(schedule_management_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id = decode_token['user_id']
        json_data = request.get_json()
        update_schedule_management_validator = update_schedule_management_schema.load(json_data)
        schedule_management = schedule_management_service.update_schedule_management(user_id=user_id, schedule_management_id=schedule_management_id, data=update_schedule_management_validator)
        schedule_management_json = schedule_management_schema.dump(obj=schedule_management)
        object_payload = simplejson.dumps(obj={'payload': schedule_management_json, 'skip_sid': user_id})
        redis_client.publish('schedule_managements.update', object_payload)
        return schedule_management_schema.jsonify(obj=schedule_management), 200
    except Exception as e:
        return jsonify(message=str(e)), 400



@schedule_management_bp.route('/api/v1/schedule-managements/schedule-shares/roadmap/share', methods=['POST'])
def handle_roadmaps_share_with_schedule():
    try:
        schedule_setup_informations = request.get_json()
        list_schedule_shares = schedule_management_share_route.handle_schedule_share(schedule_setup_informations=schedule_setup_informations)
        list_schedule_shares_dict = schedule_share_item_schema.dump(obj=list_schedule_shares, many=True)
        return jsonify(message='Success', list_schedule_share=list_schedule_shares_dict), 200
    except SQLAlchemyError as e:
        return jsonify(message='Lỗi khi thêm lộ trình vào lịch trình'), 400
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400

@schedule_management_bp.route('/api/v1/schedule-shares/<int:schedule_share_id>/roadmaps-share', methods=['GET'])
@middleware_auth
def get_all_roadmaps_share_of_schedule_share(schedule_share_id):
    id_token = request.headers.get('Authorization').split(' ')[1]
    decode_token = auth.verify_id_token(id_token=id_token)
    user_id = decode_token['user_id']
    roadmaps_share = roadmap_share_service.get_roadmaps_share_by_schedule_share_id(schedule_share_id=schedule_share_id)
    return roadmap_share_schema.jsonify(obj=roadmaps_share, many=True), 200

@schedule_management_bp.route('/api/v1/schedule-shares/<int:schedule_share_id>/roadmaps-share/is-open', methods=['GET'])
def get_roadmaps_share_of_schedule_share_is_open(schedule_share_id):
    roadmaps_share = roadmap_share_service.get_roadmaps_share_by_schedule_share_id_is_open(schedule_share_id=schedule_share_id)
    return roadmap_share_schema.jsonify(obj=roadmaps_share, many=True), 200


@schedule_management_bp.route('/api/v1/schedule-shares/<int:schedule_share_id>/roadmaps-share/<int:roadmap_share_id>/request', methods=['POST'])
def handle_request_roadmap_share(schedule_share_id, roadmap_share_id):
    json_data = request.get_json()
    try:
        validator = create_roadmap_request_validator.load(data=json_data)
        roadmap_request, notification = schedule_management_share_route.add_new_request_roadmap(validator=validator, roadmap_share_id=roadmap_share_id)
        roadmap_request_json = roadmap_request_schema.dump(obj=roadmap_request)
        notification_json = notification_schema.dump(obj=notification)

        roadmap_request_payload = simplejson.dumps(obj={'payload': roadmap_request_json, 'send_to': validator['receiver_id'], 'skip_sid': validator['sender_id']})
        notification_payload = simplejson.dumps(obj={'payload': notification_json, 'send_to': validator['receiver_id'], 'skip_sid': validator['sender_id']})
        
        redis_client.publish('roadmap_request.update', roadmap_request_payload)
        redis_client.publish('notification.update', notification_payload)

        return jsonify(message='Success'), 200
    except SQLAlchemyError as e:
        return jsonify(message=e), 400    
    except Exception as e:
        return jsonify(message=str(e)), 403    

@schedule_management_bp.route('/api/v1/roadmaps-share/<int:roadmap_share_id>/roadmap-requests', methods=['GET'])
def get_roadmaps_request_of_roadmap_share(roadmap_share_id):
    roadmap_requests = roadmap_request_service.get_roadmaps_request_by_roadmap_share_id(roadmap_share_id=roadmap_share_id)
    return roadmap_request_schema.jsonify(obj=roadmap_requests, many=True), 200

@schedule_management_bp.route('/api/v1/schedules-share/<int:schedule_share_id>', methods=['PUT'])
def update_schedule_share(schedule_share_id):
    try:
        json_data = request.get_json()
        update_schedule_share_validator = update_schedule_share_schema.load(data=json_data)

        schedule_share = schedule_management_share_route\
                        .handle_update_schedule_share(update_schedule_share_validator=update_schedule_share_validator, schedule_share_id=schedule_share_id)
        return schedule_share_item_schema.jsonify(obj=schedule_share), 200
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400

@schedule_management_bp.route('/api/v1/roadmaps-share/<int:roadmap_share_id>/roadmap-requests/<int:roadmap_request_id>/accept', methods=['POST'])
@middleware_auth
def accept_roadmap_request(roadmap_share_id, roadmap_request_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        main_user_id = decode_token['user_id']
        roadmap_requests_of_roadmap_share, notification_pairing, roadmap_share = schedule_management_share_route\
                                                                    .handle_accept_roadmap_request(roadmap_request_id, main_user_id)
        notification_pairing_json = notification_schema.dump(obj=notification_pairing)
        roadmap_share_json = roadmap_share_schema.dump(obj=roadmap_share)
    
        noti_payloads = simplejson.dumps(obj={'payload': notification_pairing_json, 'send_to': notification_pairing.main_user_id, 'skip_sid': main_user_id})
        roadmap_share_payloads = simplejson.dumps(obj={'payload': roadmap_share_json, 'skip_sid': main_user_id})
        
        redis_client.publish('notification.update', noti_payloads)
        redis_client.publish('roadmap_share.update', roadmap_share_payloads)
        return roadmap_request_schema.jsonify(obj=roadmap_requests_of_roadmap_share, many=True), 200
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400
    
@schedule_management_bp.route('/api/v1/roadmaps-share/<int:roadmap_share_id>/roadmap-requests/<int:roadmap_request_id>/decline', methods=['POST'])
@middleware_auth
def decline_roadmap_request(roadmap_share_id, roadmap_request_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        main_user_id = decode_token['user_id']
        roadmap_request = schedule_management_share_route.handle_decline_roadmap_request(roadmap_request_id, main_user_id)
        return roadmap_request_schema.jsonify(obj=roadmap_request), 200
    except Exception as e:
        return jsonify(message=str(e)), 401


@schedule_management_bp.route('/api/v1/users/<user_id>/roadmaps-request', methods=['GET'])
@middleware_auth
def get_roadmaps_request_of_user(user_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id_token = decode_token['user_id']
        if (user_id_token != user_id):
            raise Exception('Không có quyền truy cập tài nguyên không phải của bạn')
        roadmaps_request = roadmap_request_service.get_roadmaps_request_by_sender_id(sender_id=user_id)
        return roadmap_request_schema.jsonify(obj=roadmaps_request, many=True), 200
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400

@schedule_management_bp.route('/api/v1/users/<user_id>/roadmaps-request/<int:roadmap_request_id>', methods=['POST'])
@middleware_auth
def cancel_request(user_id, roadmap_request_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id_token = decode_token['user_id']
        if (user_id_token != user_id):
            raise Exception('Không có quyền truy cập tài nguyên không phải của bạn')
        roadmap_request = roadmap_request_service.update_cancel_status_roadmap_request(roadmap_request_id=roadmap_request_id)
        roadmap_request_json = roadmap_request_schema.dump(obj=roadmap_request)
        roadmap_request_json_str = simplejson.dumps(obj={'payload': roadmap_request_json, 'send_to': roadmap_request.roadmap_share.schedule_share.schedule_management.user_id, 'skip_sid': None})
        redis_client.publish('roadmap_request.update', roadmap_request_json_str)
        
        return roadmap_request_schema.jsonify(obj=roadmap_request), 200
    except Exception as e:
        return jsonify(message=str(e)), 401

        