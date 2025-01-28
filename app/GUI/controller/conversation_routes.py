from flask import Blueprint, jsonify, request
from app.GUI.model.models import Conversation
from app.Container.InstanceContainer import conversation_service, conversation_schema, message_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import join_room
from app.BLL.Redis.utils.redis_utils import redis_client
from app.Socket.controllers.socket import socketio

conversation_route_bp = Blueprint('conversation', __name__)


@conversation_route_bp.route('/api/v1/user/conversation', methods=['POST'])
# @jwt_required()
def get_conversation_id():
    json_data = request.get_json()
    first_user_id = json_data.get('first_user_id')
    second_user_id = json_data.get('second_user_id')

    conversation = conversation_service.handle_private_conversation(first_user_id=first_user_id, second_user_id=second_user_id)
    if (not conversation):
        return jsonify(error='Error when create conversation'), 400
    
    join_room(room=f'private_conversation_{conversation.conversation_id}', sid=redis_client.get(f'user_sid:{first_user_id}'), namespace='/')
    join_room(room=f'private_conversation_{conversation.conversation_id}', sid=redis_client.get(f'user_sid:{second_user_id}'), namespace='/')


    return jsonify(conversation_id=conversation.conversation_id, status='success'), 200

@conversation_route_bp.route('/api/v1/user/conversation/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = conversation_service.get_conversation_by_id(conversation_id=conversation_id)

    if (not conversation):
        return jsonify(status='failed', message='Conversation not found'), 404
    return conversation_schema.jsonify(obj=conversation), 200

@conversation_route_bp.route('/api/v1/user/<int:user_id>/conversations', methods=['GET'])
# @jwt_required()
def get_conversations_of_user(user_id):
    conversations = conversation_service.get_conversations_by_user_id(user_id=user_id)
    return conversation_schema.dump(obj=conversations, many=True), 200
    # return {}

@conversation_route_bp.route('/api/v1/user/conversations/<int:conversation_id>/cursor/<int:cursor>', methods=['GET'])
# @jwt_required()
def get_list_messages(conversation_id, cursor):
    messages = conversation_service.get_message_from_conversation(cursor=cursor, conversation_id=conversation_id)
    return message_schema.jsonify(obj=messages, many=True)




# @conversation_route_bp.route('/api/v1/user/conversations', methods=['POST'])
# def test():
#     json_data = request.get_json()
#     first_user_id = json_data.get('first_user_id')
#     second_user_id = json_data.get('second_user_id')
#     conversation = conversation_service.get_conversation_by_two_user_id(first_user_id=first_user_id, second_user_id=second_user_id)
#     return conversation_schema.jsonify(conversation)

# @conversation_route_bp.route('/api/v1/user/conversation/<int:conversation_id>/message', methods=['POST'])
# def add_message(conversation_id):
#     json_data = request.get_json()

#     content = json_data.get('content')
#     sender_id = json_data.get('sender_id')

#     message = conversation_service.add_message_to_conversation(conversation_id=conversation_id, sender_id=sender_id, content=content)
#     if (not message):
#         return jsonify(status='failed', messsage='Error when send message'), 401
    
#     message_json = message_schema.dump(obj=message)
#     socketio.emit('message.update', message_json, to=f'private_conversation_{conversation_id}')

#     return jsonify(status='success'), 200





