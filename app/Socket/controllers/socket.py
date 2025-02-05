from app.BLL.Redis.utils.redis_utils import redis_client
import simplejson
from flask_socketio import SocketIO
from flask import request
from app.GUI.model.models import Message
from app.Container.InstanceContainer import injector, message_schema
from app.BLL.Interfaces.IConversationService import IConversationService
from flask_socketio import join_room


socketio = SocketIO(json=simplejson, async_mode='gevent')
conversation_service = injector.get(interface=IConversationService)

def register_socketio_events(socketio: SocketIO):
    @socketio.on('connect')
    def test_connect():
        print(f'someone connected to websocket {request.sid}')

    @socketio.on('login success')
    def handle_success_login(data):
        redis_client.set(f'user_sid:{data}', request.sid)
        redis_client.set(f'key_user_sid:{request.sid}', data)
        
        # conversations = conversation_service.get_conversations_by_user_id(user_id=data)

        # for conversation in conversations:
        #     join_room(room=f'private_conversation_{conversation.conversation_id}', sid=request.sid, namespace='/')

        print(f'User login successful with session id: {redis_client.get(f'user_sid:{data}')}')
        print(f'User login successful with user_id: {redis_client.get(f'key_user_sid:{request.sid}')}')

    @socketio.on('send_message')
    def handle_send_message(data):
        sender_id = data['sender_id']
        content = data['content']
        conversation_id = data['conversation_id']

        conversation = conversation_service.get_conversation_by_id(conversation_id=conversation_id)
        if (not conversation):
            socketio.emit('conversation_error', {
                'status': 'error',
                'code': 'CONVERSATION_NOT_FOUND',
                'message': 'Failed to get conversation (Check conversation_id again)'
            }, to=request.sid)

        message = conversation_service.add_message_to_conversation(conversation=conversation, sender_id=sender_id, content=content)
        if (not message):
            socketio.emit('message_error', {
                'status': 'error',
                'code': 'MESSAGE_CREATION_FAILED',
                'message': 'Failed to create message'
            }, to=request.sid)
        
        message_json = message_schema.dump(obj=message)
        socketio.emit('messages.update', {'message': message_json, 'conversation_id': conversation_id}, to=f'private_conversation_{conversation_id}')
        # socketio.emit('conversation.update', {'conversation_id': conversation_id}, to=f'private_conversation_{conversation_id}')

    @socketio.on('add_user_active')
    def handle_add_active_user(data):
        users = simplejson.loads(redis_client.get('users'))
        users.append(data)
        redis_client.set('users', simplejson.dumps(obj=users))
        print("Add user active success")

    @socketio.on('get_active_users')
    def handle_get_active_users():
        users = simplejson.loads(redis_client.get('users'))
        socketio.emit('get_active_users', users)
        print("get active user")
    
    @socketio.on('logout')
    def handle_logout(data):

        users = simplejson.loads(redis_client.get('users'))
        users = [user for user in users if user['user_id'] != redis_client.get(f'key_user_sid:{request.sid}')]
        redis_client.set('users', simplejson.dumps(obj=users))

        redis_client.delete(f'user_sid:{redis_client.get(f'key_user_sid:{request.sid}')}')
        redis_client.delete(f'key_user_sid:{request.sid}')
        print(f'User {data} logout: {request.sid}')

    @socketio.on('disconnect')
    def test_disconnect():
        print(f'User disconnected (user_sid: {request.sid}, user_id: {redis_client.get(f'key_user_sid:{request.sid}')})')
        users = simplejson.loads(redis_client.get('users'))
        users = [user for user in users if user['user_id'] != redis_client.get(f'key_user_sid:{request.sid}')]
        redis_client.set('users', simplejson.dumps(obj=users))

        redis_client.delete(f'user_sid:{redis_client.get(f'key_user_sid:{request.sid}')}')
        redis_client.delete(f'key_user_sid:{request.sid}')

# @socketio.on('connect')
# def test_connect():
#     print(f'someone connected to websocket {request.sid}')
    

# @socketio.on('login success')
# def handle_success_login(data):
#     redis_client[f'userId:{data}'] = request.sid 
#     print(f'User login successful with session id: {request.sid}')
    
# @socketio.on('logout')
# def handle_logout(data):
#     redis_client.delete(f'userId:{data}')
#     print(f'User {data} logout: {request.sid}')

# @socketio.on('disconnect')
# def test_disconnect():
#     print('someone disconnected')
    