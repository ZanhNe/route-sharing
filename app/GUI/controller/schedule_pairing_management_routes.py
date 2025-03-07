from flask import Blueprint, jsonify, request
from app.Container.InstanceContainer import injector,\
      schedule_pairing_management_schema, roadmap_pairing_schema, roadmap_pairing_request_schema, notification_schema
from app.BLL.Redis.utils.redis_utils import redis_client
from app.BLL.Interfaces.ISchedulePairingManagementService import ISchedulePairingManagementService
from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService
from app.BLL.Interfaces.IRoadmapPairingRequestService import IRoadmapPairingRequestService
from app.BLL.Interfaces.IScheduleManagementShareRoute import IScheduleManagementShareRoute


from app.decorator.decorator import middleware_auth
from firebase_admin import auth
import simplejson

schedule_pairing_management_bp = Blueprint('schedule-pairing-management', __name__)
schedule_pairing_management_service = injector.get(interface=ISchedulePairingManagementService)
roadmap_pairing_service = injector.get(interface=IRoadmapPairingService)
roadmap_pairing_request_service = injector.get(interface=IRoadmapPairingRequestService)
schedule_management_share_route = injector.get(interface=IScheduleManagementShareRoute)

@schedule_pairing_management_bp.route('/api/v1/users/<user_id>/schedule-pairing-managements', methods=['GET'])
@middleware_auth
def get_schedule_pairing_management_of_user(user_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token, clock_skew_seconds=10)
        if (user_id != decode_token['user_id']):
            raise Exception('Không có quyền truy cập vào tài nguyên của người khác')
        schedule_pairing_management = schedule_pairing_management_service.get_schedule_pairing_management_of_user(user_id=user_id)
        return schedule_pairing_management_schema.jsonify(obj=schedule_pairing_management), 200
    except Exception as e:
        return jsonify(message=str(e)), 401
    
@schedule_pairing_management_bp.route('/api/v1/schedule-pairings/<int:schedule_pairing_id>/roadmap-pairings', methods=['GET'])
def get_roadmap_pairings_of_schedule_pairing(schedule_pairing_id):
    try:
        id_token = request.headers.get('Authorization').split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token, clock_skew_seconds=10)
        roadmaps_pairing = roadmap_pairing_service.get_roadmaps_pairing_by_schedule_pairing_id(schedule_pairing_id=schedule_pairing_id, user_id=decode_token['user_id'])
        return roadmap_pairing_schema.jsonify(obj=roadmaps_pairing, many=True), 200
    except Exception as e:
        return jsonify(message=str(e)), 400
    
@schedule_pairing_management_bp.route('/api/v1/roadmaps-pairing/<int:roadmap_pairing_id>/is-start', methods=['POST'])
@middleware_auth
def handle_start_roadmap(roadmap_pairing_id):
    try:
        id_token = request.headers['Authorization'].split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id_token = decode_token['user_id']

        main_user_roadmaps_pairing\
        , secondary_user_roadmaps_pairing\
        , secondary_user_roadmaps_pairing_request_send\
        , secondary_user_roadmaps_pairing_request_receive, list_user_id = schedule_management_share_route.handle_start_roadmap_pairing(user_id=user_id_token, roadmap_pairing_id=roadmap_pairing_id)
        
        secondary_user_roadmaps_pairing_json = roadmap_pairing_schema.dump(obj=secondary_user_roadmaps_pairing, many=True)
        secondary_user_roadmaps_pairing_payloads = simplejson.dumps(obj={'payload': secondary_user_roadmaps_pairing_json, 'send_to': list_user_id[1], 'skip_sid': list_user_id[0]})

        secondary_user_roadmaps_pairing_request_send_json = roadmap_pairing_request_schema.dump(obj=secondary_user_roadmaps_pairing_request_send, many=True)
        secondary_user_roadmaps_pairing_request_send_payloads = simplejson.dumps(obj={'payload': secondary_user_roadmaps_pairing_request_send_json, 'send_to': list_user_id[1], 'skip_sid': list_user_id[0]})

        secondary_user_roadmaps_pairing_request_receive_json = roadmap_pairing_request_schema.dump(obj=secondary_user_roadmaps_pairing_request_receive, many=True)
        secondary_user_roadmaps_pairing_request_receive_payloads = simplejson.dumps(obj={'payload': secondary_user_roadmaps_pairing_request_receive_json, 'send_to': list_user_id[1], 'skip_sid': list_user_id[0]})
        

        redis_client.publish('roadmap_pairing.update', secondary_user_roadmaps_pairing_payloads)
        redis_client.publish('roadmap_pairing.update', secondary_user_roadmaps_pairing_request_send_payloads)
        redis_client.publish('roadmap_pairing.update', secondary_user_roadmaps_pairing_request_receive_payloads)

        return roadmap_pairing_schema.jsonify(obj=main_user_roadmaps_pairing, many=True), 200
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 400

@schedule_pairing_management_bp.route('/api/v1/roadmaps-pairing/<roadmap_pairing_id>/is-end', methods=['POST'])
@middleware_auth
def handle_end_roadmap(roadmap_pairing_id):
    try:
        id_token = request.headers['Authorization'].split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id_token = decode_token['user_id']
        
        roadmap_pairing = schedule_management_share_route.handle_end_roadmap_pairing(user_id=user_id_token, roadmap_pairing_id=roadmap_pairing_id)
        roadmap_pairing_json = roadmap_pairing_schema.dump(obj=roadmap_pairing)
        roadmap_pairing_payloads = simplejson.dumps(obj={'payload': roadmap_pairing_json, 'skip_sid': user_id_token, 'send_to': roadmap_pairing.roadmap_request.sender_id})


        redis_client.publish('roadmap_pairing.update', roadmap_pairing_payloads)
        return roadmap_pairing_schema.jsonify(obj=roadmap_pairing), 200
    except Exception as e:
        return jsonify(message=str(e)), 401


@schedule_pairing_management_bp.route('/api/v1/roadmaps-pairing/<int:roadmap_pairing_id>/send-request', methods=['POST'])
@middleware_auth
def send_request_roadmap_pairing(roadmap_pairing_id):
    try:   
        id_token = request.headers['Authorization'].split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        sender_id = decode_token['user_id']
        roadmap_pairing_request, notification = schedule_management_share_route.send_roadmap_pairing_request(sender_id=sender_id, roadmap_pairing_id=roadmap_pairing_id)
        
        notification_json = notification_schema.dump(obj=notification)
        noti_payloads = simplejson.dumps(obj={'payload': notification_json, 'send_to': roadmap_pairing_request.roadmap_pairing.roadmap_request.sender_id, 'skip_sid': sender_id})
        redis_client.publish('notification.update', noti_payloads)
        return roadmap_pairing_request_schema.jsonify(obj=roadmap_pairing_request), 200
    except Exception as e:
        return jsonify(message=str(e)), 400

@schedule_pairing_management_bp.route('/api/v1/roadmaps-pairing/<int:roadmap_pairing_id>/roadmaps-pairing-request/<int:roadmap_pairing_request_id>/accept', methods=['POST'])
@middleware_auth
def accept_roadmap_pairing_request(roadmap_pairing_id, roadmap_pairing_request_id):
    try:
        id_token = request.headers['Authorization'].split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        secondary_user_id = decode_token['user_id']

        roadmap_pairing, notification = schedule_management_share_route.accept_roadmap_pairing_request(secondary_user_id=secondary_user_id, roadmap_pairing_id=roadmap_pairing_id, roadmap_pairing_request_id=roadmap_pairing_request_id)
        notification_json = notification_schema.dump(obj=notification)
        noti_payloads = simplejson.dumps(obj={'payload': notification_json, 'send_to': notification.main_user_id, 'skip_sid': notification.secondary_user_id})
        redis_client.publish('notification.update', noti_payloads)
        return roadmap_pairing_schema.jsonify(obj=roadmap_pairing), 200
    except Exception as e:
        return jsonify(message=str(e)), 400
    
@schedule_pairing_management_bp.route('/api/v1/roadmaps-pairing/<int:roadmap_pairing_id>/roadmaps-pairing-request/<int:roadmap_pairing_request_id>/decline', methods=['POST'])
@middleware_auth
def decline_roadmap_pairing_request(roadmap_pairing_id, roadmap_pairing_request_id):
    try:
        id_token = request.headers['Authorization'].split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        secondary_user_id = decode_token['user_id']

        roadmap_pairing, notification = schedule_management_share_route.decline_roadmap_pairing_request(secondary_user_id=secondary_user_id, roadmap_pairing_request_id=roadmap_pairing_request_id)
        notification_json = notification_schema.dump(obj=notification)
        noti_payloads = simplejson.dumps(obj={'payload': notification_json, 'send_to': notification.main_user_id, 'skip_sid': notification.secondary_user_id})
        redis_client.publish('notification.update', noti_payloads)
        return roadmap_pairing_schema.jsonify(obj=roadmap_pairing), 200
    except Exception as e:
        return jsonify(message=str(e)), 400


@schedule_pairing_management_bp.route('/api/v1/users/<user_id>/roadmaps-pairing-request/is-received', methods=['GET'])
@middleware_auth
def get_roadmaps_pairing_request_of_user_receive(user_id):
    try:
        id_token = request.headers['Authorization'].split(' ')[1]
        decode_token = auth.verify_id_token(id_token=id_token)
        user_id_token = decode_token['user_id']
        if (user_id_token != user_id):
            raise Exception('Không có quyền truy cập tài nguyên user khác')
        roadmaps_pairing_request = roadmap_pairing_request_service.get_roadmaps_pairing_request_by_secondary_user(secondary_user=user_id_token)
        return roadmap_pairing_request_schema.jsonify(obj=roadmaps_pairing_request, many=True), 200
    except Exception as e:
        print(e)
        return jsonify(message=str(e)), 401
    
@schedule_pairing_management_bp.route('/api/v1/roadmaps-pairing/<int:roadmap_pairing_id>/roadmaps-pairing-request', methods=['GET'])
def get_roadmaps_pairing_request_of_roadmap_pairing(roadmap_pairing_id):
    try:
        roadmap_pairing = roadmap_pairing_service.get_roadmap_pairing_by_id(roadmap_pairing_id=roadmap_pairing_id)
        roadmaps_pairing_request = roadmap_pairing.list_roadmap_pairing_request
        return roadmap_pairing_request_schema.jsonify(obj=roadmaps_pairing_request, many=True), 200
    except Exception as e:
        return jsonify(message=str(e)), 401

