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
            'schedule_managements.update': self.schedule_managements_handler,
            'roadmap_request.update': self.roadmap_request_handler,
            'join_private_conversation': None
        }
    
    def routes_share_socket_handler(self, data, to: str = None, skip_sid: str = None):
        if (not to):
            self.socketio.emit('routes_share.update', data, skip_sid=skip_sid)
        else:
            self.socketio.emit('routes_share.update', data, to=to, skip_sid=skip_sid)

    def request_route_socket_handler(self, data, to: str = None, skip_sid: str = None):
        if (not to):
            self.socketio.emit('request_route.update', data, skip_sid=skip_sid)
        else:
            self.socketio.emit('request_route.update', data, to=to, skip_sid=skip_sid)

    def notification_socket_handler(self, data, to: str = None, skip_sid: str = None):
        if (not to):
            self.socketio.emit('notification.update', data, skip_sid=skip_sid)
        else:
            self.socketio.emit('notification.update', data, to=to, skip_sid=skip_sid)

    def user_socket_handler(self, data, to: str = None, skip_sid: str = None):
        if (not to):
            self.socketio.emit('user.update', data, skip_sid=skip_sid)
        else:
            self.socketio.emit('user.update', data, to=to, skip_sid=skip_sid)      

    def schedule_managements_handler(self, data, to: str = None, skip_sid: str = None):
        if (not to):
            self.socketio.emit('schedule_managements.update', data, skip_sid=skip_sid)
        else:
            self.socketio.emit('schedule_managements.update', data, to=to, skip_sid=skip_sid)
    
    def roadmap_request_handler(self, data, to: str = None, skip_sid: str = None):
        if (not to):
            self.socketio.emit('roadmap_request.update', data, skip_sid=skip_sid)
        else:
            self.socketio.emit('roadmap_request.update', data, to=to, skip_sid=skip_sid)
        