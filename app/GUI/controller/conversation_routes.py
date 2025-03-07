from flask import Blueprint, jsonify, request
from app.GUI.model.models import Conversation
from app.Container.InstanceContainer import injector, conversation_schema, message_schema
from app.BLL.Interfaces.IConversationService import IConversationService
from flask_socketio import join_room
from app.decorator.decorator import middleware_auth
from app.BLL.Redis.utils.redis_utils import redis_client

conversation_route_bp = Blueprint('conversation', __name__)
conversation_service = injector.get(interface=IConversationService)


@conversation_route_bp.route('/api/v1/user/conversation', methods=['POST'])
@middleware_auth
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


@conversation_route_bp.route('/api/v1/user/conversations/<int:conversation_id>/cursor/<int:cursor>', methods=['GET'])
def get_list_messages(conversation_id, cursor):
    messages = conversation_service.get_message_from_conversation(cursor=cursor, conversation_id=conversation_id)
    return message_schema.jsonify(obj=messages, many=True)

@conversation_route_bp.route('/api/v1/user/<user_id>/conversations', methods=['GET'])
def get_conversations_of_user(user_id):
    conversations = conversation_service.get_conversations_by_user_id(user_id=user_id)
    return conversation_schema.jsonify(obj=conversations, many=True), 200






