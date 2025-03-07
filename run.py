

from app import flask_app
from app.extentions.extentions import socketio
from app.Socket.controllers.socket import register_socketio_events
from app.BLL.Redis.utils.redis_utils import redis_client, CHANNELS
from app.BLL.Redis.Services.RedisService import RedisService
from app.Socket.handlers.handler.SocketHandler import SocketHandler
import threading


socket_handler = SocketHandler(socketio=socketio)
register_socketio_events(socketio=socketio)
redis_service = RedisService(redis_client=redis_client, socket_handler=socket_handler, app=flask_app)


thread = threading.Thread(target=redis_service.start_subsrcibe, args=(CHANNELS,), daemon=True)
thread.start()


if __name__ == '__main__':
    socketio.run(debug=False, use_reloader=False, app=flask_app)
