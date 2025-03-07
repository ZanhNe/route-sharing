from app.extentions.extentions import ma
from app.GUI.model.models import Participant, Conversation, Message, User, Roles, Location, Route, Place,\
                                 Notification, ScheduleManagement, ScheduleShare, RoadmapShare, RoadmapRequest, SchedulePairingManagement, \
                                 SchedulePairing, RoadmapPairing, RoadmapPairingRequest
from marshmallow import fields, validates, ValidationError, post_dump, validate
# from flask_marshmallow import Marshmallow
import simplejson



class LinkNotificationValidator(ma.Schema):
    url = fields.Str(required=True, validate=validate.Length(min=21), error_messages={'required': 'Vui lòng điền đủ đường dẫn URL, tối thiểu 21 kí tự'})

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
#         load_instance = Trues

class CreateRoadmapRequestValidator(ma.Schema):
    sender_id = fields.Str(required=True, validate=validate.Length(min=4))
    receiver_id = fields.Str(required=True, validate=validate.Length(min=4))
    list_place_id = fields.List(fields.Str(), validate=validate.Length(min=2))

class UpdateScheduleManagementValidator(ma.Schema):
    title = fields.Str(required=True, error_messages={'required': 'Vui lòng điền đủ tiêu đề (title)'})
    content = fields.Str(required=True, error_messages={'required': 'Vui lòng điền đủ nội dung (content)'})
    is_open = fields.Bool()
    
class UpdateScheduleShareValidator(ma.Schema):
    departure_date = fields.Str(required=True, error_messages={'required': 'Vui lòng chọn ngày khởi hành'})
    is_open = fields.Bool()




class ParticipantSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))

    class Meta:
        model = Participant
        load_instance = True
        render_module = simplejson
    
    last_viewed = fields.DateTime(format='iso')
    


class ConversationSchema(ma.SQLAlchemyAutoSchema):
    messages = ma.Nested('MessageSchema', many=True)
    participants = ma.Nested('ParticipantSchema', many=True)
    class Meta:
        model = Conversation
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')
    lastest_updated = fields.DateTime(format='iso')

class MessageSchema(ma.SQLAlchemyAutoSchema):
    sender = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
    class Meta:
        model = Message
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')
    

class ScheduleManagementSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
    list_schedule_shares = ma.Nested('ScheduleShareItemSchema', many=True)
    class Meta:
        model = ScheduleManagement
        load_instance = True
        render_module = simplejson
    title = fields.Str(required=True, error_messages={'required': 'Vui lòng điền đủ tiêu đề (title)'})
    content = fields.Str(required=True, error_messages={'required': 'Vui lòng điền đủ nội dung (content)'})
    created_date = fields.DateTime(format='iso')

    @validates('title')
    def validate_title(self, title):
        if (len(title) < 3):
            raise ValidationError('Tiêu đề phải tối thiểu 3 kí tự')
        if (len(title) > 255):
            raise ValidationError('Tiêu đề phải tối đa 255 kí tự')
        
    
    @validates('content')
    def validate_content(self, content):
        if (len(content) < 10):
            raise ValidationError('Tiêu đề phải tối thiểu 10 kí tự')
        
    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for schedule_management in data:
                schedule_management['created_date'] = f'{schedule_management['created_date']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
        
        return data



class BaseScheduleShareSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScheduleShare
        load_instance = True
        render_module = simplejson

    created_date = fields.DateTime(format='iso')
    departure_date = fields.DateTime(format='iso')

    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for schedule_share in data:
                print(schedule_share)
                schedule_share['created_date'] = f'{schedule_share['created_date']}+07:00'
                schedule_share['departure_date'] = f'{schedule_share['departure_date']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
            data['departure_date'] = f'{data['departure_date']}+07:00'
        
        return data

class ScheduleShareItemSchema(BaseScheduleShareSchema):
    class Meta(BaseScheduleShareSchema.Meta):
        include_fk = True

    

class ScheduleShareSchema(BaseScheduleShareSchema):
    schedule_management = ma.Nested('ScheduleManagementSchema', exclude=('list_schedule_shares',))
    list_roadmaps = ma.Nested('RoadmapShareSchema', many=True, exclude=('schedule_share',))
    
    

class RoadmapShareSchema(ma.SQLAlchemyAutoSchema):
    schedule_share = ma.Nested('ScheduleShareSchema', exclude=('list_roadmaps',))
    route = ma.Nested('RouteSchema')
    roadmap_requests = ma.Nested('RoadmapRequestSchema', many=True, exclude=('roadmap_share',))
    class Meta:
        model = RoadmapShare
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')
    estimated_departure_time = fields.DateTime(format='iso')
    estimated_arrival_time = fields.DateTime(format='iso')

    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for schedule_share in data:
                schedule_share['created_date'] = f'{schedule_share['created_date']}+07:00'
                schedule_share['estimated_departure_time'] = f'{schedule_share['estimated_departure_time']}+07:00'
                schedule_share['estimated_arrival_time'] = f'{schedule_share['estimated_arrival_time']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
            data['estimated_departure_time'] = f'{data['estimated_departure_time']}+07:00'
            data['estimated_arrival_time'] = f'{data['estimated_arrival_time']}+07:00'
        
        return data

class RoadmapRequestSchema(ma.SQLAlchemyAutoSchema):
    roadmap_share = ma.Nested('RoadmapShareSchema', exclude=('roadmap_requests',))
    sender = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar'))
    route = ma.Nested('RouteSchema')
    class Meta:
        model = RoadmapRequest
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')

    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for roadmap_request in data:
                roadmap_request['created_date'] = f'{roadmap_request['created_date']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
        
        return data

    

class SchedulePairingManagementSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
    list_schedule_pairings = ma.Nested('SchedulePairingItemSchema', many=True)
    class Meta:
        model = SchedulePairingManagement
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')

# class UserRoadmapPairingSchema(ma.SQLAlchemyAutoSchema):
#     user = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
#     roadmap_pairing = ma.Nested('RoadmapPairingSchema', exclude=('list_user_pairings',))
#     class Meta:
#         model = UserRoadmapPairing
#         load_instance = True
#         render_module = simplejson
#     joined_date = fields.DateTime(format='iso')

class SchedulePairingItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SchedulePairing
        load_instance = True
        render_module = simplejson
        include_fk = True
    created_date = fields.DateTime(format='iso')
    departure_date = fields.DateTime(format='iso')

class SchedulePairingSchema(ma.SQLAlchemyAutoSchema):
    schedule_pairing_management = ma.Nested('SchedulePairingManagementSchema', exclude=('list_schedule_pairings',))
    list_roadmap_pairings = ma.Nested('RoadmapPairingSchema', many=True, exclude=('list_schedule_pairings',))
    class Meta:
        model = SchedulePairing
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')
    departure_date = fields.DateTime(format='iso')

class RoadmapPairingSchema(ma.SQLAlchemyAutoSchema):
    route = ma.Nested('RouteSchema')
    roadmap_request = ma.Nested('RoadmapRequestSchema')
    class Meta:
        model = RoadmapPairing
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')
    actual_departure_time = fields.DateTime(format='iso')
    actual_arrival_time = fields.DateTime(format='iso')

    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for roadmap_pairing in data:
                roadmap_pairing['created_date'] = f'{roadmap_pairing['created_date']}+07:00'
                if (roadmap_pairing['actual_departure_time']):
                    roadmap_pairing['actual_departure_time'] = f'{roadmap_pairing['actual_departure_time']}+07:00'
                if (roadmap_pairing['actual_arrival_time']):
                    roadmap_pairing['actual_arrival_time'] = f'{roadmap_pairing['actual_arrival_time']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
            if (data['actual_departure_time']):
                data['actual_departure_time'] = f'{data['actual_departure_time']}+07:00'
            if (data['actual_arrival_time']):
                data['actual_arrival_time'] = f'{data['actual_arrival_time']}+07:00'
        return data

class RoadmapPairingRequestSchema(ma.SQLAlchemyAutoSchema):
    roadmap_pairing = ma.Nested('RoadmapPairingSchema')
    sender = ma.Nested('UserSchema', only=('user_id', 'user_name', 'avatar',))
    class Meta:
        model = RoadmapPairingRequest
        load_instance = True
        render_module = simplejson
    created_date = fields.DateTime(format='iso')

    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for roadmap_pairing_request in data:
                roadmap_pairing_request['created_date'] = f'{roadmap_pairing_request['created_date']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
        
        return data



class UserSchema(ma.SQLAlchemyAutoSchema):
    roles = ma.Nested('RoleSchema', many=True, exclude=('users',))
    notifications = ma.Nested('NotiSchema', many=True, exclude=('sender', 'receiver',))
    list_schedule_managements = ma.Nested('ScheduleManagementSchema', many=True, exclude=('user',))
    roadmap_requests = ma.Nested('RoadmapRequestSchema', many=True, exclude=('sender',))
    list_roadmap_pairings = ma.Nested('UserRoadmapPairingSchema', many=True, exclude=('user',))

    class Meta: 
        model = User
        render_module = simplejson
        load_instance = True

    created_time = fields.DateTime(format='iso')
        

class NotificationSchema(ma.SQLAlchemyAutoSchema):
    main_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="main_user")
    secondary_user = ma.Nested(lambda: UserSchema(only=("user_id", "user_name", "avatar")), attribute="secondary_user")
    class Meta:
        model = Notification
        render_module = simplejson
        load_instance = True
    created_date = fields.DateTime(format='iso')

    @post_dump(pass_many=True)
    def add_utc_z(self, data, many, **kwargs):
        if many:
            for noti in data:
                noti['created_date'] = f'{noti['created_date']}+07:00'
        else:
            data['created_date'] = f'{data['created_date']}+07:00'
        
        return data

    

class LocationSchema(ma.SQLAlchemyAutoSchema):
    place = ma.Nested('PlaceSchema', exclude=('location',))
    class Meta:
        model = Location
        render_module = simplejson
        load_instance = True 

class PlaceSchema(ma.SQLAlchemyAutoSchema):
    location = ma.Nested('LocationSchema', exclude=('place',))
    class Meta:
        model = Place
        render_module = simplejson
        load_instance = True

class RouteSchema(ma.SQLAlchemyAutoSchema):
    places = ma.Nested('PlaceSchema', many=True)
    class Meta:
        model = Route
        render_module = simplejson
        load_instance = True
    

