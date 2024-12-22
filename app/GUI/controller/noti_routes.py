from flask import Blueprint, jsonify, request
from app.GUI.model.models import Notification
from app.Container.InstanceContainer import notification_service, notification_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_route_bp = Blueprint('notification', __name__)

@notification_route_bp.route('/api/v1/user/notification', methods=['GET'])
@jwt_required()
def get_notification_of_user():
    identity = get_jwt_identity()
    notifications_user = notification_service.get_all_notifications_of_user(user_id=identity['user_id'])
    return notification_schema.jsonify(obj=notifications_user, many=True), 200
    # pprint.pprint(identity)
    # return 'Test'