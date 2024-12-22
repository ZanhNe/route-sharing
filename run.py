
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





