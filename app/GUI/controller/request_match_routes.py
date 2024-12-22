from flask import Blueprint, jsonify, request
from app.GUI.model.models import RequestRoute
from app.Container.InstanceContainer import request_route_service, request_route_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

request_match_bp = Blueprint('request_match', __name__)

@request_match_bp.route('/api/v1/user/request/main')
@jwt_required()
def get_requests_main_user():
    identity = get_jwt_identity()
    main_user_id = identity['user_id']

    requests_match_main_user = request_route_service.get_requests_route_main_user_pending(main_user_id=main_user_id)
    return request_route_schema.jsonify(obj=requests_match_main_user, many=True), 200

@request_match_bp.route('/api/v1/user/request/secondary')
@jwt_required()
def get_requests_secondary_user():
    identity = get_jwt_identity()
    main_user_id = identity['user_id']
    
    requests_match_secondary_user = request_route_service.get_requests_route_secondary_user_pending(secondary_user_id=main_user_id)
    return request_route_schema.jsonify(obj=requests_match_secondary_user, many=True), 200
