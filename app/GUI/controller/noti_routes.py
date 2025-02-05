from flask import Blueprint, jsonify, request
from app.GUI.model.models import Notification
from app.Container.InstanceContainer import injector, notification_schema
from app.BLL.Interfaces.INotificationService import INotificationService
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_route_bp = Blueprint('notification', __name__)
notification_service = injector.get(interface=INotificationService)

@notification_route_bp.route('/api/v1/users/<user_id>/notification', methods=['GET'])
def get_notification_of_user(user_id):
    notifications_user = notification_service.get_all_notifications_of_user(user_id=user_id)
    return notification_schema.jsonify(obj=notifications_user, many=True), 200
    # pprint.pprint(identity)
    # return 'Test'