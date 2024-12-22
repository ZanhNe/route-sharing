
# from gevent import monkey
# monkey.patch_all()

from app import create_app
from app.Socket.controllers.socket import socketio, register_socketio_events
from app.BLL.Redis.utils.redis_utils import redis_client, CHANNELS
from app.BLL.Redis.Services.RedisService import RedisService
from app.Socket.handlers.handler.SocketHandler import SocketHandler
import threading



app = create_app()
socket_handler = SocketHandler(socketio=socketio)
redis_service = RedisService(redis_client=redis_client, socket_handler=socket_handler)


thread = threading.Thread(target=redis_service.start_subsrcibe, args=(CHANNELS,), daemon=True)
thread.start()

register_socketio_events(socketio=socketio)



if __name__ == '__main__':
    socketio.run(app=app, debug=True, use_reloader=False)




# def handle_redis_message(message):
#     try:
#         print("Đang emit message:", message)  # Debug log
#         socketio.emit('route_share.update', message)
#         print("Đã emit xong")  # Debug log
#     except Exception as e:
#         print("Lỗi khi emit:", str(e))  # Catch lỗi

# def start_subsrcibe():
#     pubsub = redis_client.pubsub()
#     pubsub.subscribe('route_share.update')

#     print("Subscribe channel")

#     while True:
#         message = pubsub.get_message(ignore_subscribe_messages=True)
#         if (not message):
#             time.sleep(0.1)
#         else:
#             try:
#                 data = simplejson.loads(message['data'])
#                 handle_redis_message(message=data)
#             except Exception as e:
#                 print(e) 
       
# import eventlet
# eventlet.monkey_patch()  # Thực hiện monkey_patch() trước

# import redis
# from flask import Flask
# from flask_socketio import SocketIO

# app = Flask(__name__)

# # Kết nối Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# socketio = SocketIO(app, message_queue='redis://localhost:6379/0', async_mode='eventlet')

# try:
#     redis_client.ping()
#     print("Redis connected")
# except Exception as e:
#     print("Cannot connect to Redis:", e)

# @socketio.on('message')
# def handle_message(msg):
#     print(f"Received message: {msg}")
#     redis_client.publish('my_channel', msg)  # Gửi message vào Redis

# @socketio.on('connect')
# def handle_connect():
#     print("Connected")


# if __name__ == '__main__':
#     socketio.run(app, debug=True)


