
from app.extentions.extentions import db
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Numeric, Enum
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
import enum



route_location = Table('route_location', 
                        db.metadata, 
                        Column('route_id', ForeignKey('route.route_id'), primary_key=True), 
                        Column('location_id', ForeignKey('location.location_id'), primary_key=True))

RouteDetail = Table('routedetail', db.metadata,
                    Column('route_id', ForeignKey('route.route_id'), primary_key=True),
                    Column('place_id', ForeignKey('place.place_id'), primary_key=True),
                    Column('order', Integer, nullable=True))

user_role = Table('user_role', db.metadata, 
                    Column('user_id', ForeignKey('user.user_id'), primary_key=True), 
                    Column('role_id', ForeignKey('roles.role_id'), primary_key=True))

user_location = Table('user_location', db.metadata,
                        Column('user_id', ForeignKey('user.user_id'), primary_key=True),
                        Column('location_id', ForeignKey('location.location_id'), primary_key=True))

user_route = Table('user_route', db.metadata,
                    Column('user_id', ForeignKey('user.user_id'), primary_key=True),
                    Column('route_id', ForeignKey('route.route_id'), primary_key=True))



class Status(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    CANCELLED = 'cancelled'
    FREE = 'free'


class StatusMatch(enum.Enum):
    WAITING = 'waiting'
    COMPLETED = 'completed'
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    CANCELLED = 'cancelled'

class StatusActive(enum.Enum):
    CLOSE = 'close'
    OPEN = 'open'

# Định nghĩa enum cho các loại notification
class NotificationType(enum.Enum):
    REQUEST = 'request'
    OTHER = "other"



class BaseParticipant(db.Model):
    __abstract__ = True
    participant_id: Mapped[int] = mapped_column('participant_id', primary_key=True, autoincrement=True)
    last_viewed: Mapped[Optional[DateTime]] = mapped_column('last_viewed', DateTime, default=datetime.now, nullable=False)
    user_id: Mapped[str] = mapped_column('user_id', ForeignKey('user.user_id'))




class Participant(BaseParticipant, db.Model):
    __tablename__ = 'participant'
    conversation_id: Mapped[int] = mapped_column('conversation_id', ForeignKey('conversation.conversation_id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='participates', lazy=True)
    conversation: Mapped['Conversation'] = relationship(back_populates='participants', lazy=True)

class ParticipantGroup(BaseParticipant, db.Model):
    __tablename__ = 'participant_group'
    joined_date: Mapped[DateTime] = mapped_column('joined_date', DateTime)
    conversation_group_id: Mapped[int] = mapped_column('conversation_group_id', ForeignKey('conversation_group.conversation_id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='participate_groups', lazy=True)
    conversation_group: Mapped['ConversationGroup'] = relationship(back_populates='participants', lazy=True)


class BaseConversation(db.Model):
    __abstract__ = True
    conversation_id: Mapped[int] = mapped_column('conversation_id', primary_key=True, autoincrement=True)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    lastest_updated: Mapped[DateTime] = mapped_column('lastest_updated', DateTime, default=datetime.now, nullable=True)

class Conversation(BaseConversation, db.Model):
    __tablename__ = 'conversation'

    messages: Mapped[List['Message']] = relationship(lazy=True)
    participants: Mapped[List['Participant']] = relationship(back_populates='conversation', lazy=True)

class ConversationGroup(BaseConversation, db.Model):
    __tablename__ = 'conversation_group'
    conversation_name: Mapped[str] = mapped_column('conversation_name', String(1000), nullable=False)
    photo: Mapped[Optional[str]] = mapped_column('photo', String(1000), nullable=True)

    # created_by_id: Mapped[int] = mapped_column('created_by_id', ForeignKey('user.user_id'))
    # created_by: Mapped['User'] = relationship(back_populates='host_groups', lazy=True)

    messages: Mapped[List['MessageGroup']] = relationship(lazy=True)
    participants: Mapped[List['ParticipantGroup']] = relationship(lazy=True)







class BaseMessage(db.Model):
    __abstract__ = True
    message_id: Mapped[int] = mapped_column('message_id', primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column('content', LONGTEXT(charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)    
    sender_id: Mapped[str] = mapped_column('sender_id', ForeignKey('user.user_id'))

    @declared_attr
    def sender(cls) -> Mapped['User']:
        return relationship(foreign_keys=[cls.sender_id], lazy='select')

    # sender: Mapped['User'] = relationship(foreign_keys=[sender_id])


class Message(BaseMessage, db.Model):
    __tablename__ = 'message'
    conversation_id: Mapped[int] = mapped_column('conversation_id', ForeignKey('conversation.conversation_id'))


class MessageGroup(BaseMessage, db.Model):
    __tablename__ = 'message_group'
    
    group_id: Mapped[int] = mapped_column('group_id', ForeignKey('conversation_group.conversation_id'))






class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id: Mapped[int] = mapped_column('notification_id', primary_key=True, autoincrement=True)

    content: Mapped[str] = mapped_column('content', String(1000), nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    is_read: Mapped[bool] = mapped_column('is_read', default=False, nullable=False)
    
    main_user_id: Mapped[str] = mapped_column('main_user_id', ForeignKey('user.user_id'))
    secondary_user_id: Mapped[str] = mapped_column('secondary_user_id', ForeignKey('user.user_id'))

    main_user: Mapped['User'] = relationship(back_populates='notification_associations', foreign_keys=[main_user_id], lazy=True)
    secondary_user: Mapped['User'] = relationship(foreign_keys=[secondary_user_id])




class Roles(db.Model):
    __tablename__ = 'roles'
    role_id : Mapped[int] = mapped_column('role_id', primary_key=True, autoincrement=True)
    role_name : Mapped[Optional[str]] = mapped_column('role_name', String(20), nullable=True)
    users: Mapped[List['User']] = relationship(secondary=user_role, back_populates='roles', lazy=True)


class Location(db.Model):
    __tablename__ = 'location'
    location_id : Mapped[int] = mapped_column('location_id', primary_key=True, autoincrement=True)
    latitude: Mapped[float] = mapped_column('latitude', Numeric(10, 7), nullable=False)
    longitude: Mapped[float] = mapped_column('longitude', Numeric(10, 7), nullable=False)
    place_id: Mapped[int] = mapped_column(ForeignKey('place.place_id'), nullable=True)
    place: Mapped['Place'] = relationship(back_populates='location', lazy=True)


class Place(db.Model):
    __tablename__ = 'place'
    place_id: Mapped[str] = mapped_column('place_id', String(200), primary_key=True)
    formatt_address: Mapped[str] = mapped_column('address', String(1000), nullable=False)
    location: Mapped['Location'] = relationship(uselist=False, back_populates='place', lazy=True)
    routes: Mapped[List['Route']] = relationship(secondary=RouteDetail, back_populates='places', lazy=True)

  


class Route(db.Model):
    __tablename__ = 'route'
    route_id: Mapped[int] = mapped_column('route_id', primary_key=True, autoincrement=True)
    route_name: Mapped[str] = mapped_column('route_name', String(500), nullable=False)
    places: Mapped[List['Place']] = relationship(secondary=RouteDetail, back_populates='routes', lazy=True, order_by='routedetail.c.order')


class ScheduleManagement(db.Model):
    __tablename__ = 'schedule_management'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column('title', String(500), nullable=False)
    content: Mapped[str] = mapped_column('content', LONGTEXT(charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False)
    is_open: Mapped[bool] = mapped_column('is_open', default=True, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('user.user_id'), nullable=True)

    user: Mapped['User'] = relationship(back_populates='list_schedule_managements', lazy=True)
    list_schedule_shares: Mapped[List['ScheduleShare']] = relationship(back_populates='schedule_management'\
                                                                       , order_by='ScheduleShare.departure_date'\
                                                                       ,cascade='all, delete'\
                                                                        , lazy=True)



class ScheduleShare(db.Model):
    __tablename__ = 'schedule_share'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    # status: Mapped[str] = mapped_column('status', Enum(StatusActive), default=StatusActive.OPEN, nullable=False)
    is_open: Mapped[bool] = mapped_column('is_open', default=True, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    departure_date: Mapped[DateTime] = mapped_column('departure_date', DateTime, nullable=False)

    schedule_management_id: Mapped[int] = mapped_column('schedule_management_id', ForeignKey('schedule_management.id'))
    
    schedule_management: Mapped['ScheduleManagement'] = relationship(back_populates='list_schedule_shares', lazy=True)
    list_roadmaps: Mapped[List['RoadmapShare']] = relationship(back_populates='schedule_share'\
                                                               , lazy=True\
                                                               , cascade='all, delete'\
                                                                , order_by='RoadmapShare.estimated_departure_time')

    def checkValidRoadmapFromAnotherTime(self, time) -> bool:
        if (not len(self.list_roadmaps)):
            return True
        dt1 = self.list_roadmaps[len(self.list_roadmaps) - 1].estimated_arrival_time
        dt2 = datetime.fromisoformat(time)
        return dt2 >= dt1
    
    def logAllRoadmaps(self) -> None:
        print("Ngày khởi hành dự kiến: ", self.departure_date)
        for roadmap in self.list_roadmaps:
            print("=================================")
            print("Thời gian bắt đầu dự kiến: ", roadmap.estimated_departure_time)
            print("Thời gian kết thúc dự kiến: ", roadmap.estimated_arrival_time)
            print("=================================")


class RoadmapShare(db.Model):
    __tablename__ = 'roadmap_share'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    # status: Mapped[str] = mapped_column('status', Enum(StatusActive), default=StatusActive.OPEN, nullable=False)
    is_open: Mapped[bool] = mapped_column('is_open', default=True, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    estimated_departure_time: Mapped[DateTime] = mapped_column('estimated_departure_time', DateTime, nullable=False) #Giờ khởi hành dự kiến
    estimated_arrival_time: Mapped[DateTime] = mapped_column('estimated_arrival_time', DateTime, nullable=False) #Giờ đến nơi dự kiến

    schedule_share_id: Mapped[int] = mapped_column('schedule_share_id', ForeignKey('schedule_share.id'))
    route_id: Mapped[int] = mapped_column('route_id', ForeignKey('route.route_id'))

    schedule_share: Mapped['ScheduleShare'] = relationship(back_populates='list_roadmaps', lazy=True)
    route: Mapped['Route'] = relationship(lazy=True)
    roadmap_requests: Mapped[List['RoadmapRequest']] = relationship(back_populates='roadmap_share'\
                                                                    , cascade='all, delete'\
                                                                    , lazy=True)


class RoadmapRequest(db.Model):
    __tablename__ = 'roadmap_request'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column('status', Enum(Status), default=Status.PENDING, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)

    roadmap_share_id: Mapped[int] = mapped_column('roadmap_share_id', ForeignKey('roadmap_share.id'))
    sender_id: Mapped[int] = mapped_column('sender_id', ForeignKey('user.user_id'))
    route_id: Mapped[int] = mapped_column('route_id', ForeignKey('route.route_id'))

    roadmap_share: Mapped['RoadmapShare'] = relationship(back_populates='roadmap_requests', lazy=True)

    roadmap_pairing: Mapped[Optional['RoadmapPairing']] = relationship(back_populates='roadmap_request', cascade='delete', lazy=True)

    sender: Mapped['User'] = relationship(back_populates='roadmap_requests', lazy=True) 
    route: Mapped['Route'] = relationship(lazy=True)

class SchedulePairingManagement(db.Model):
    __tablename__ = 'schedule_pairing_management'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)

    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('user.user_id'))

    user: Mapped['User'] = relationship(lazy=True)
    list_schedule_pairings: Mapped[List['SchedulePairing']] = relationship(back_populates='schedule_pairing_management', lazy=True)    

schedulepairing_roadmappairing = Table('schedulepairing_roadmappairing', db.metadata, 
                    Column('schedule_pairing_id', ForeignKey('schedule_pairing.id', ondelete='CASCADE'), primary_key=True), 
                    Column('roadmap_pairing_id', ForeignKey('roadmap_pairing.id', ondelete='CASCADE'), primary_key=True))



class SchedulePairing(db.Model):
    __tablename__ = 'schedule_pairing'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    is_open: Mapped[bool] = mapped_column('is_open', default=True, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    departure_date: Mapped[DateTime] = mapped_column('departure_date', DateTime, nullable=False)

    schedule_pairing_management_id: Mapped[int] = mapped_column('schedule_pairing_management_id', ForeignKey('schedule_pairing_management.id'))
    
    schedule_pairing_management: Mapped['SchedulePairingManagement'] = relationship(back_populates='list_schedule_pairings', lazy=True)
    list_roadmap_pairings: Mapped[List['RoadmapPairing']] = relationship(secondary=schedulepairing_roadmappairing, back_populates='list_schedule_pairings', lazy='dynamic')

class RoadmapPairing(db.Model):
    __tablename__ = 'roadmap_pairing'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column('status', Enum(StatusMatch), default=StatusMatch.NOT_STARTED, nullable=False)
    # is_open: Mapped[bool] = mapped_column('is_open', default=True, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)
    actual_departure_time: Mapped[Optional[DateTime]] = mapped_column('actual_departure_time', DateTime, nullable=True) #Giờ khởi hành dự kiến
    actual_arrival_time: Mapped[Optional[DateTime]] = mapped_column('actual_arrival_time', DateTime, nullable=True) #Giờ đến nơi dự kiến  

    roadmap_request_id: Mapped[int] = mapped_column('roadmap_request_id', ForeignKey('roadmap_request.id'))
    
    roadmap_request: Mapped['RoadmapRequest'] = relationship(back_populates='roadmap_pairing', cascade='delete', lazy=True)
    list_roadmap_pairing_request: Mapped[List['RoadmapPairingRequest']] = relationship(back_populates='roadmap_pairing', cascade='all, delete', lazy=True)
    list_schedule_pairings: Mapped[List['SchedulePairing']] = relationship(secondary=schedulepairing_roadmappairing, back_populates='list_roadmap_pairings', lazy='dynamic')

    def check_roadmap_pairing_request(self) -> bool:
        if (not len(self.list_roadmap_pairing_request)):
            return True
        if (self.list_roadmap_pairing_request[-1].status == Status.PENDING):
            return False
        return True


class RoadmapPairingRequest(db.Model):
    __tablename__ = 'roadmap_pairing_request'
    id: Mapped[int] = mapped_column('id', primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column('status', Enum(Status), default=Status.PENDING, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now, nullable=False)

    roadmap_pairing_id: Mapped[int] = mapped_column('roadmap_pairing_id', ForeignKey('roadmap_pairing.id'))
    sender_id: Mapped[int] = mapped_column('sender_id', ForeignKey('user.user_id'))

    roadmap_pairing: Mapped['RoadmapPairing'] = relationship(back_populates='list_roadmap_pairing_request', lazy=True)
    sender: Mapped['User'] = relationship(back_populates='roadmap_pairing_requests', lazy=True)

    


class User(db.Model):
    __tablename__ = 'user'
    user_id: Mapped[str] = mapped_column('user_id', String(200), primary_key=True)
    user_name: Mapped[str] = mapped_column('username', String(30), nullable=True)
    user_account: Mapped[str] = mapped_column('user_account', String(30), nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column('avatar', String(300), nullable=True)
    background: Mapped[str] = mapped_column('background', String(300), nullable=True)
    phone: Mapped[str] = mapped_column('phone', String(11), unique=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column('is_verified', default=False, nullable=True) #TODO ---------
    status : Mapped[str] = mapped_column('status', Enum(Status), default=Status.FREE)
    created_time: Mapped[DateTime] = mapped_column('created_time', DateTime, default=datetime.now, nullable=True)
    updated_time: Mapped[Optional[DateTime]] = mapped_column('updated_time', DateTime, nullable=True)


    roles: Mapped[List['Roles']] = relationship(secondary='user_role', back_populates='users', cascade='delete')


    participates: Mapped[List['Participant']] = relationship(back_populates='user', lazy=True, cascade='delete')
    participate_groups: Mapped[List['ParticipantGroup']] = relationship(back_populates='user', lazy=True, cascade='delete')

    notification_associations: Mapped[List['Notification']] = relationship(foreign_keys=[Notification.main_user_id], back_populates='main_user', cascade='delete', lazy=True)
    list_schedule_managements: Mapped[List['ScheduleManagement']] = relationship(back_populates='user', lazy=True, cascade='delete')
    roadmap_requests: Mapped[List['RoadmapRequest']] = relationship(back_populates='sender', lazy=True, cascade='delete')
    roadmap_pairing_requests: Mapped[List['RoadmapPairingRequest']] = relationship(back_populates='sender', lazy=True, cascade='delete')







