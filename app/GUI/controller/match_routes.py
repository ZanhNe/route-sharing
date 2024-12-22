from flask import Blueprint, jsonify, request
from app.GUI.model.models import RequestRoute
from app.Container.InstanceContainer import match_route_service, match_route_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

match_route_bp = Blueprint('match', __name__)

@match_route_bp.route('/api/v1/user/match/main', methods=['GET'])
@jwt_required()
def get_list_match_main_user():
    matchs = match_route_service.get_list_match_main_user(main_user_id=get_jwt_identity()['user_id'])
    return match_route_schema.jsonify(obj=matchs, many=True), 200