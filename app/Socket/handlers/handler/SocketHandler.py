from app.Socket.handlers.Interfaces.ISocketHandler import ISocketHandler
from flask_socketio import SocketIO

class SocketHandler(ISocketHandler):
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.handlers = {
            'routes_share.update': self.routes_share_socket_handler,
            'request_route.update': self.request_route_socket_handler,
            'notification.update': self.notification_socket_handler,
            'user.update': self.user_socket_handler,
            'join_private_conversation': None
        }
    
    def routes_share_socket_handler(self, data, to: str = None):
        if (not to):
            self.socketio.emit('routes_share.update', data)
        else:
            self.socketio.emit('routes_share.update', data, to=to)

    def request_route_socket_handler(self, data, to: str = None):
        if (not to):
            self.socketio.emit('request_route.update', data)
        else:
            self.socketio.emit('request_route.update', data, to=to)

    def notification_socket_handler(self, data, to: str = None):
        if (not to):
            self.socketio.emit('notification.update', data)
        else:
            self.socketio.emit('notification.update', data, to=to)

    def user_socket_handler(self, data, to: str = None):
        if (not to):
            self.socketio.emit('user.update', data)
        else:
            self.socketio.emit('user.update', data, to=to)      

    
        