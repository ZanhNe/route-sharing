from app.GUI.model.models import Conversation, Message, User, Roles, Location, Route, Bus, BusTicket, Payment, MatchRoute, Place, UserRouteShare, RequestRoute, Notification
from marshmallow import fields, validate
from flask_marshmallow import Marshmallow
import simplejson

ma = Marshmallow()

class RoleSchema(ma.SQLAlchemyAutoSchema):
    users = ma.Nested('UserSchema', many=True, exclude=('roles',))
    class Meta:
        model = Roles
        load_instance = True

# class NotiSchema(ma.SQLAlchemyAutoSchema):
#     sender = ma.Nested('UserSchema', exclude=('notifications',))
#     receiver = ma.Nested('UserSchema', exclude=('notifications',))
#     class Meta:
#         model = Notification
#         load_instance = True

# class RequestRouteSchema(ma.SQLAlchemyAutoSchema):
#     sender_location = ma.Nested('LocationSchema')
#     sender = ma.Nested('UserSchema', exclude=('request_routes',))
#     receiver = ma.Nested('UserSchema', exclude=('request_routes',))
#     class Meta:
#         model = RequestRoute
#         load_instance = True

#     main_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="main_user")
#     secondary_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="secondary_user")
#     class Meta:
#         model = MatchRoute
#         load_instance = True

class ConversationSchema(ma.SQLAlchemyAutoSchema):
    messages = ma.Nested('MessageSchema', many=True)
    main_user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
    secondary_user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
    class Meta:
        model = Conversation
        load_instance = True
        render_module = simplejson

class MessageSchema(ma.SQLAlchemyAutoSchema):
    sender = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar'))
    class Meta:
        model = Message
        load_instance = True
        render_module = simplejson

# class ConversationMemberSchema(ma.SQLAlchemyAutoSchema):
#     conversation = ma.Nested('ConversationSchema', exclude=('members', 'messages',))
#     member = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar'))
#     class Meta:
#         model = ConversationMember
#         load_instance = True
#         render_module = simplejson

class UserSchema(ma.SQLAlchemyAutoSchema):
    # matches = ma.Nested('UserSchema', many=True, exclude=('matches',))
    roles = ma.Nested('RoleSchema', many=True, exclude=('users',))
    match_associations = ma.Nested('MatchRouteSchema', many=True, exclude=('main_user',))
    # locations = ma.Nested('LocationSchema', many=True, exclude=('users',))
    bus = ma.Nested('BusSchema', exclude=('users',))
    tickets = ma.Nested('TicketSchema', many=True, exclude=('users',))
    payments = ma.Nested('PaymentSchema', many=True, exclude=('user',))
    # posts = ma.Nested('PostSchema', many=True, exclude=('user',))
    # comments = ma.Nested('CommentSchema', many=True, exclude=('user',))
    routes_share = ma.Nested('UserRouteShareSchema', many=True, exclude=('user',))
    notifications = ma.Nested('NotiSchema', many=True, exclude=('sender', 'receiver',))
    request_routes = ma.Nested('RequestRouteSchema', many=True, exclude=('sender', 'receiver',))
    # match_routes = ma.Nested('MatchRouteSchema', many=True, exclude=('sender', 'receiver'))

    class Meta: 
        model = User
        render_module = simplejson
        load_instance = True
        

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    main_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="main_user")
    secondary_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="secondary_user")
    class Meta:
        model = Notification
        render_module = simplejson
        load_instance = True

class RequestRouteSchema(ma.SQLAlchemyAutoSchema):
    main_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="main_user")
    secondary_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="secondary_user")
    route = ma.Nested('RouteSchema')    
    class Meta:
        model = RequestRoute
        render_module = simplejson
        load_instance = True

    
class MatchRouteSchema(ma.SQLAlchemyAutoSchema):
    main_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="main_user")
    secondary_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="secondary_user")
    route = ma.Nested('RouteSchema', exclude=('matchs',))
    class Meta:
        model = MatchRoute
        render_module = simplejson
        load_instance = True

class UserRouteShareSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar'))
    route = ma.Nested('RouteSchema')
    class Meta:
        model = UserRouteShare
        render_module = simplejson
        load_instance = True

class LocationSchema(ma.SQLAlchemyAutoSchema):
    place = ma.Nested('PlaceSchema', exclude=('location',))
    class Meta:
        model = Location
        render_module = simplejson
        load_instance = True 

class PlaceSchema(ma.SQLAlchemyAutoSchema):
    # routes = ma.Nested('RouteSchema', many=True, exclude=('places',))
    location = ma.Nested('LocationSchema', exclude=('place',))
    class Meta:
        model = Place
        render_module = simplejson
        load_instance = True

class RouteSchema(ma.SQLAlchemyAutoSchema):
    # users_share = ma.Nested('UserRouteShareSchema', many=True, exclude=('route',))
    places = ma.Nested('PlaceSchema', many=True)
    # buses = ma.Nested('BusSchema', many=True, exclude=('route',))
    # matchs = ma.Nested('MatchRouteSchema', many=True, exclude=('route',))
    class Meta:
        model = Route
        render_module = simplejson
        load_instance = True
    
class BusSchema(ma.SQLAlchemyAutoSchema):
    route = ma.Nested('RouteSchema')
    users = ma.Nested('UserSchema', many=True, exclude=('bus',))
    tickets = ma.Nested('TicketSchema', many=True, exclude=('buses',))
    class Meta:
        model = Bus
        render_module = simplejson
        load_instance = True

class TicketSchema(ma.SQLAlchemyAutoSchema):
    buses = ma.Nested('BusSchema', many=True, exclude=('tickets',))
    users = ma.Nested('UserSchema', many=True, exclude=('tickets',))
    class Meta:
        model = BusTicket
        render_module = simplejson
        load_instance = True

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested('UserSchema', exclude=('payments',))
    class Meta: 
        model = Payment
        load_instance = True


# class PostSchema(ma.SQLAlchemyAutoSchema):
#     user = ma.Nested('UserSchema', exclude=('posts',))
#     comments = ma.Nested('CommentSchema', exclude=('post',))
#     class Meta:
#         model = Post
#         load_instance = True

# class CommentSchema(ma.SQLAlchemyAutoSchema):
#     user = ma.Nested('UserSchema', exclude=('comments',))
#     # post = ma.Nested('PostSchema', exclude=('comments',))
#     class Meta:
#         model = Comment
#         load_instance = True

