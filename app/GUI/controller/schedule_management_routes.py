from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.Container.InstanceContainer import schedule_management_service\
                                    , schedule_management_schema, route_place_service, schedule_share_item_schema, roadmap_share_service\
                                    , roadmap_share_schema, create_roadmap_request_validator, notification_service, roadmap_request_service\
                                    , roadmap_request_schema, notification_schema
                                    
from app.BLL.Redis.utils.redis_utils import redis_client
import simplejson

from app.BLL.Services.ScheduleManagementShareRoute import ScheduleManagementShareRoute


schedule_management_bp = Blueprint('schedule_management', __name__)

@schedule_management_bp.route('/api/v1/schedule-managements/users/<user_id>', methods=['GET'])
def get_all_schedule_managements_of_user(user_id):
    schedule_managements = schedule_management_service.get_all_schedule_management_by_user_id(user_id=user_id)
    return schedule_management_schema.jsonify(obj=schedule_managements, many=True), 200

@schedule_management_bp.route('/api/v1/schedule-managements/<int:schedule_management_id>', methods=['GET'])
def get_schedule_management_of_user(schedule_management_id):
    schedule_management = schedule_management_service.get_schedule_management_by_schedule_management_id(schedule_management_id=schedule_management_id)
    return schedule_management_schema.jsonify(obj=schedule_management), 200

@schedule_management_bp.route('/api/v1/schedule-managements/users/<user_id>', methods=['POST'])
def create_schedule_management_for_user(user_id):
    json_data = request.get_json()
    try:
        scheduleManagementMapper = schedule_management_schema.load(data=json_data)
        scheduleManagementMapper.user_id = user_id
        scheduleManagementCreate = schedule_management_service.create_schedule_management(schedule_management=scheduleManagementMapper)
        scheduleManagementCreateJson = schedule_management_schema.dump(obj=scheduleManagementCreate)
        dataObjectPayload = simplejson.dumps({'payload': scheduleManagementCreateJson})
        # print(dataObjectPayload)
        redis_client.publish('schedule_managements.update', message=dataObjectPayload)
        return jsonify(message='Tao thanh cong'), 201
    except ValidationError as ve:
        print(ve.messages)
        return jsonify({"errors": ve.messages['content']}), 422
    except SQLAlchemyError as sae:
        return jsonify({"errors": str(sae)}), 500
    except Exception as ex:
        return jsonify({"errors": str(ex)}), 500

@schedule_management_bp.route('/api/v1/schedule-managements/is-open', methods=['GET'])
def get_all_schedule_managements_opening():
    schedule_managements = schedule_management_service.get_all_schedule_managements_opening()
    return schedule_management_schema.jsonify(obj=schedule_managements, many=True), 200

@schedule_management_bp.route('/api/v1/schedule-managements/<int:schedule_management_id>/closed')
def set_close_schedule_management(schedule_management_id):
    pass

@schedule_management_bp.route('/api/v1/schedule-managements/schedule-shares/roadmap/share', methods=['POST'])
def handle_roadmaps_share_with_schedule():
    try:
        schedule_management_share_route_service = ScheduleManagementShareRoute(route_place_service=route_place_service\
                                                    , schedule_management_service=schedule_management_service\
                                                    , notification_service=notification_service, roadmap_request_service=roadmap_request_service)
        schedule_setup_informations = request.get_json()
        list_schedule_shares = schedule_management_share_route_service.handle_schedule_share(schedule_setup_informations=schedule_setup_informations)
        list_schedule_shares_dict = schedule_share_item_schema.dump(obj=list_schedule_shares, many=True)
        return jsonify(message='Success', list_schedule_share=list_schedule_shares_dict), 200
        # return schedule_share_schema.jsonify(obj=list_schedule_shares, many=True), 200
    except SQLAlchemyError as e:
        return jsonify(message='Lỗi khi thêm lộ trình vào lịch trình'), 400
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400

@schedule_management_bp.route('/api/v1/schedule-shares/<int:schedule_share_id>/roadmaps-share', methods=['GET'])
def get_all_roadmaps_share_of_schedule_share(schedule_share_id):
    roadmaps_share = roadmap_share_service.get_roadmaps_share_by_schedule_share_id(schedule_share_id=schedule_share_id)
    return roadmap_share_schema.jsonify(obj=roadmaps_share, many=True), 200


@schedule_management_bp.route('/api/v1/schedule-shares/<int:schedule_share_id>/roadmaps-share/<int:roadmap_share_id>/request', methods=['POST'])
def handle_request_roadmap_share(schedule_share_id, roadmap_share_id):
    json_data = request.get_json()
    try:
        validator = create_roadmap_request_validator.load(data=json_data)
        schedule_management_share_route_service = ScheduleManagementShareRoute(route_place_service=route_place_service\
                                                    , schedule_management_service=schedule_management_service\
                                                    , notification_service=notification_service, roadmap_request_service=roadmap_request_service)
        roadmap_request, notification = schedule_management_share_route_service.add_new_request_roadmap(validator=validator, roadmap_share_id=roadmap_share_id)
        roadmap_request_json = roadmap_request_schema.dump(obj=roadmap_request)
        notification_json = notification_schema.dump(obj=notification)

        roadmap_request_payload = simplejson.dumps(obj={'payload': roadmap_request_json, 'send_to': validator['receiver_id'], 'include_self': False})
        notification_payload = simplejson.dumps(obj={'payload': notification_json, 'send_to': validator['receiver_id'], 'include_self': False})
        
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




        