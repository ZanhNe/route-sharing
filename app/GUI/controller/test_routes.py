from flask import Flask, request, jsonify, Blueprint
from app.Container.InstanceContainer import user_schema, injector
from app.BLL.Interfaces.IUserService import IUserService
from app.GUI.model.models import db

test_bp = Blueprint('test', __name__)
user_service = injector.get(interface=IUserService)

@test_bp.route('/api/v1/test/users/<id>', methods=['GET'])
def test_get_user(id):
    user = user_service.get_user_by_id(session=db.session, user_id=id)
    return user_schema.jsonify(obj=user), 200

