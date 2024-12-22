# from app.extentions.extentions import db
from typing import Optional, List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Table, Numeric, Enum
from datetime import datetime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.dialects.mysql import LONGTEXT
import enum


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


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

bus_ticket = Table('bus_ticket', db.metadata,
                    Column('bus_id', ForeignKey('bus.bus_id'), primary_key=True),
                    Column('ticket_id', ForeignKey('busticket.ticket_id'), primary_key=True))

class Status(enum.Enum):
    FREE = 'free'
    MATCHING = 'matching'
    PENDING = 'pending'
    WAITING = 'waiting'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    CANCELLED = 'cancelled'

# Định nghĩa enum cho các loại notification
class NotificationType(enum.Enum):
    REQUEST = 'request'
    OTHER = "other"


class UserTicket(db.Model):
    __tablename__ = 'user_ticket'
    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('user.user_id'), primary_key=True)
    ticket_id: Mapped[int] = mapped_column('ticket_id', ForeignKey('busticket.ticket_id'), primary_key=True)
    status: Mapped[bool] = mapped_column('status', default=False, nullable=False)

    user: Mapped['User'] = relationship(back_populates='tickets', lazy=True)
    ticket: Mapped['BusTicket'] = relationship(back_populates='users', lazy=True)



class BaseConversation(db.Model):
    __abstract__ = True
    conversation_id: Mapped[int] = mapped_column('conversation_id', primary_key=True, autoincrement=True)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now(), nullable=False)

class Conversation(BaseConversation, db.Model):
    __tablename__ = 'conversation'

    main_user_id: Mapped[int] = mapped_column('main_user_id', ForeignKey('user.user_id'))
    secondary_user_id: Mapped[int] = mapped_column('secondary_user_id', ForeignKey('user.user_id'))

    messages: Mapped[List['Message']] = relationship()
    main_user: Mapped['User'] = relationship(foreign_keys=[main_user_id], back_populates='conversation_associations', lazy=True)
    secondary_user: Mapped['User'] = relationship(foreign_keys=[secondary_user_id], lazy=True)

class ConversationGroup(BaseConversation, db.Model):
    __tablename__ = 'conversation_group'
    conversation_name: Mapped[str] = mapped_column('conversation_name', String(1000), nullable=False)
    photo: Mapped[Optional[str]] = mapped_column('photo', String(1000), nullable=True)

    created_by_id: Mapped[int] = mapped_column('created_by_id', ForeignKey('user.user_id'))
    created_by: Mapped['User'] = relationship(back_populates='host_groups', lazy=True)

    messages: Mapped[List['MessageGroup']] = relationship()
    members: Mapped[List['GroupMember']] = relationship(back_populates='group', lazy=True)



class GroupMember(db.Model):
    __tablename__ = 'group_member'
    infor_id: Mapped[int] = mapped_column('infor_id', primary_key=True, autoincrement=True)
    joined_date: Mapped[DateTime] = mapped_column('joined_date', DateTime, default=datetime.now())

    group_id: Mapped[int] = mapped_column('group_id', ForeignKey('conversation_group.conversation_id'))
    member_id: Mapped[int] = mapped_column('member_id', ForeignKey('user.user_id'))

    group: Mapped['ConversationGroup'] = relationship(back_populates='members', lazy=True)
    member: Mapped['User'] = relationship(back_populates='groups', lazy=True)




class BaseMessage(db.Model):
    __abstract__ = True
    message_id: Mapped[int] = mapped_column('message_id', primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column('content', LONGTEXT(charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now(), nullable=False)
    
    sender_id: Mapped[int] = mapped_column('sender_id', ForeignKey('user.user_id'))

    @declared_attr
    def sender(cls) -> Mapped['User']:
        return relationship(foreign_keys=[cls.sender_id], lazy=True)

    # sender: Mapped['User'] = relationship(foreign_keys=[sender_id])


class Message(BaseMessage, db.Model):
    __tablename__ = 'message'
    conversation_id: Mapped[int] = mapped_column('conversation_id', ForeignKey('conversation.conversation_id'))


class MessageGroup(BaseMessage, db.Model):
    __tablename__ = 'message_group'
    
    group_id: Mapped[int] = mapped_column('group_id', ForeignKey('conversation_group.conversation_id'))


class MatchRoute(db.Model):
    __tablename__ = 'matchroute'
    match_id: Mapped[int] = mapped_column('match_id', primary_key=True, autoincrement=True)

    matched_time: Mapped[DateTime] = mapped_column('matched_time', DateTime, default=datetime.now())
    is_match: Mapped[bool] = mapped_column('is_match', default=True)

    main_user_id: Mapped[int] = mapped_column('main_user_id', ForeignKey('user.user_id'))
    secondary_user_id: Mapped[int] = mapped_column('secondary_user_id', ForeignKey('user.user_id'))
    route_id: Mapped[int] = mapped_column('route_id', ForeignKey('route.route_id'))

    main_user: Mapped['User'] = relationship(back_populates='match_associations', foreign_keys=[main_user_id], lazy=True)
    secondary_user: Mapped['User'] = relationship(foreign_keys=[secondary_user_id])
    route: Mapped['Route'] = relationship(back_populates='matchs', lazy=True)


class RequestRoute(db.Model):
    __tablename__ = 'request'
    request_id: Mapped[int] = mapped_column('request_id', primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column('status', Enum(Status), default=Status.PENDING)

    created_time: Mapped[DateTime] = mapped_column('created_time', DateTime, default=datetime.now())

    main_user_id: Mapped[int] = mapped_column('main_user_id', ForeignKey('user.user_id'))
    secondary_user_id: Mapped[int] = mapped_column('secondary_user_id', ForeignKey('user.user_id'))
    route_id: Mapped[int] = mapped_column('route_id', ForeignKey('route.route_id'))

    main_user: Mapped['User'] = relationship(back_populates='request_associations', foreign_keys=[main_user_id], lazy=True)
    secondary_user: Mapped['User'] = relationship(foreign_keys=[secondary_user_id])
    route: Mapped['Route'] = relationship(back_populates='requests', lazy=True)


class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id: Mapped[int] = mapped_column('notification_id', primary_key=True, autoincrement=True)
    noti_type: Mapped[str] = mapped_column('noti_type', Enum(NotificationType), nullable=False)

    content: Mapped[str] = mapped_column('content', String(1000), nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, default=datetime.now(), nullable=False)
    is_read: Mapped[bool] = mapped_column('is_read', default=False, nullable=False)
    
    main_user_id: Mapped[int] = mapped_column('main_user_id', ForeignKey('user.user_id'))
    secondary_user_id: Mapped[int] = mapped_column('secondary_user_id', ForeignKey('user.user_id'))

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
    buses: Mapped[List["Bus"]] = relationship(back_populates='route', lazy=True)
    places: Mapped[List['Place']] = relationship(secondary=RouteDetail, back_populates='routes', lazy=True, order_by='routedetail.c.order')
    users_share: Mapped[List['UserRouteShare']] = relationship(back_populates='route', lazy=True)
    matchs: Mapped[List['MatchRoute']] = relationship(back_populates='route', lazy=True)

    requests: Mapped[List['RequestRoute']] = relationship(back_populates='route', lazy=True)

class UserRouteShare(db.Model):
    __tablename__ = 'routeshare'
    share_id: Mapped[int] = mapped_column('share_id', primary_key=True, autoincrement=True)
    is_matched: Mapped[bool] = mapped_column('is_match', default=False, nullable=False)
    share_name: Mapped[str] = mapped_column('share_name', String(255), nullable=False)
    share_description: Mapped[str] = mapped_column('share_description', LONGTEXT(charset='utf8mb4', collation='utf8mb4_unicode_ci'), nullable=False)
    share_date: Mapped[DateTime] = mapped_column('share_date', DateTime, default=datetime.now(), nullable=False)


    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('user.user_id'))
    route_id: Mapped[int] = mapped_column('route_id', ForeignKey('route.route_id'))

    user: Mapped['User'] = relationship(back_populates='routes_share', lazy=True)
    route: Mapped['Route'] = relationship(back_populates='users_share', lazy=True)


    
    
    
 


class Bus(db.Model):
    __tablename__ = 'bus'
    bus_id: Mapped[int] = mapped_column('bus_id', primary_key=True, autoincrement=True)
    bus_name: Mapped[str] = mapped_column('bus_name', String(100), nullable=False)
    route_id: Mapped[int] = mapped_column('route_id', ForeignKey('route.route_id'), nullable=True)
    route: Mapped['Route'] = relationship(back_populates='buses', lazy=True)
    users: Mapped[List['User']] = relationship(back_populates='bus', lazy=True)
    tickets: Mapped[List['BusTicket']] = relationship(secondary='bus_ticket', back_populates='buses', lazy=True)

class User(db.Model):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column('user_id', primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column('username', String(30), nullable=False)
    user_account: Mapped[str] = mapped_column('user_account', String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column('password', String(1000), nullable=False)
    avatar: Mapped[str] = mapped_column('avatar', String(300), nullable=True)
    background: Mapped[str] = mapped_column('background', String(300), nullable=True)
    status : Mapped[str] = mapped_column('status', Enum(Status), default=Status.FREE)
    created_time: Mapped[DateTime] = mapped_column('created_time', DateTime, default=datetime.now(), nullable=True)
    updated_time: Mapped[DateTime] = mapped_column('updated_time', DateTime, nullable=True)


    bus_id: Mapped[int] = mapped_column(ForeignKey('bus.bus_id'), nullable=True)
    bus: Mapped['Bus'] = relationship(back_populates='users', lazy=True)
    roles: Mapped[List['Roles']] = relationship(secondary='user_role', back_populates='users')

    routes_share: Mapped[List['UserRouteShare']] = relationship(back_populates='user', lazy=True)

    tickets: Mapped[List['UserTicket']] = relationship(back_populates='user', lazy=True)
    payments: Mapped[List['Payment']] = relationship(back_populates='user', lazy=True)

    host_groups: Mapped[List['ConversationGroup']] = relationship(back_populates='created_by', lazy=True)

    groups: Mapped[List['GroupMember']] = relationship(back_populates='member', lazy=True)

    conversation_associations: Mapped[List['Conversation']] = relationship(foreign_keys=[Conversation.main_user_id], back_populates='main_user', lazy=True)
    # secondary_conversation: Mapped[]

    match_associations: Mapped[List['MatchRoute']] = relationship(foreign_keys=[MatchRoute.main_user_id], back_populates='main_user', lazy=True)
    # secondary_match: Mapped[List['User']] = relationship(secondary='matchroute', primaryjoin=user_id==MatchRoute.main_user_id, secondaryjoin=user_id==MatchRoute.secondary_user_id, viewonly=True)

    request_associations: Mapped[List['RequestRoute']] = relationship(foreign_keys=[RequestRoute.main_user_id], back_populates='main_user', lazy=True)
    # secondary_request: Mapped[List['User']] = relationship(secondary='request', primaryjoin=user_id==RequestRoute.main_user_id, secondaryjoin=user_id==RequestRoute.secondary_user_id, viewonly=True)
    # route_shares: Mapped[List['UserShare']] = relationship(back_populates='user', lazy=True)

    notification_associations: Mapped[List['Notification']] = relationship(foreign_keys=[Notification.main_user_id], back_populates='main_user', lazy=True)
    # secondary_notification: Mapped[List['User']] = relationship(secondary='notification', primaryjoin=user_id==Notification.main_user_id, secondaryjoin=user_id==Notification.secondary_user_id, viewonly=True)
    


class BusTicket(db.Model):
    __tablename__ = 'busticket'
    ticket_id: Mapped[int] = mapped_column('ticket_id', primary_key=True, autoincrement=True)
    arrival_date: Mapped[DateTime] = mapped_column('arrival_date', DateTime, nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, nullable=False)

    users: Mapped[List['UserTicket']] = relationship(back_populates='ticket', lazy=True)
    buses: Mapped[List['Bus']] = relationship(secondary='bus_ticket', back_populates='tickets', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payment'
    pay_id: Mapped[int] = mapped_column('pay_id', primary_key=True, autoincrement=True)
    total: Mapped[float] = mapped_column('total', nullable=False)
    created_date: Mapped[DateTime] = mapped_column('created_date', DateTime, nullable=False)

    user_id: Mapped[int] = mapped_column('user_id', ForeignKey('user.user_id'), nullable=True)
    user: Mapped['User'] = relationship(back_populates='payments', lazy=True)








    


