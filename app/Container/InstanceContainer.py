from app.extentions.extentions import db
from app.custom.Helper.Helper import TransactionManager
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.ILocationRepository import ILocationRepository
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from app.DAL.Interfaces.IRoutePlaceRepository import IRoutePlaceRepository
from app.DAL.Interfaces.IPlaceRepository import IPlaceRepository
from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from app.DAL.Interfaces.IConversationRepository import IConversationRepository
from app.DAL.Interfaces.IScheduleManagementRepository import IScheduleManagementRepository
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from app.DAL.Interfaces.IRoadmapRequestRepository import IRoadmapRequestRepository
from app.DAL.Interfaces.ISchedulePairingManagementRepository import ISchedulePairingManagementRepository
from app.DAL.Interfaces.ISchedulePairingRepository import ISchedulePairingRepository
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from app.DAL.Interfaces.IRoadmapPairingRequestRepository import IRoadmapPairingRequestRepository




from app.DAL.Repositories.RoleRepository import RoleRepository
from app.DAL.Repositories.UserRepository import UserRepository
from app.DAL.Repositories.LocationRepository import LocationRepository
from app.DAL.Repositories.RouteRepository import RouteRepository
from app.DAL.Repositories.RoutePlaceRepository import RoutePlaceRepository
from app.DAL.Repositories.PlaceRepository import PlaceRepository
from app.DAL.Repositories.NotificationRepository import NotificationRepository
from app.DAL.Repositories.ConversationRepository import ConversationRepository
from app.DAL.Repositories.ScheduleManagementRepository import ScheduleManagementRepository
from app.DAL.Repositories.ScheduleShareRepository import ScheduleShareRepository
from app.DAL.Repositories.RoadmapShareRepository import RoadmapShareRepository
from app.DAL.Repositories.RoadmapRequestRepository import RoadmapRequestRepository
from app.DAL.Repositories.SchedulePairingManagementRepository import SchedulePairingManagementRepository
from app.DAL.Repositories.SchedulePairingRepository import SchedulePairingRepository
from app.DAL.Repositories.RoadmapPairingRepository import RoadmapPairingRepository
from app.DAL.Repositories.RoadmapPairingRequestRepository import RoadmapPairingRequestRepository


from app.BLL.Interfaces.IRoleService import IRoleService
from app.BLL.Interfaces.IUserService import IUserService
from app.BLL.Interfaces.IRoutePlaceService import IRoutePlaceService
from app.BLL.Interfaces.IPlaceService import IPlaceService
from app.BLL.Interfaces.INotificationService import INotificationService
from app.BLL.Interfaces.IConversationService import IConversationService
from app.BLL.Interfaces.IScheduleManagementService import IScheduleManagementService
from app.BLL.Interfaces.IRoadmapShareService import IRoadmapShareService
from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.BLL.Interfaces.IScheduleManagementShareRoute import IScheduleManagementShareRoute
from app.BLL.Interfaces.IScheduleShareService import IScheduleShareService
from app.BLL.Interfaces.ISchedulePairingManagementService import ISchedulePairingManagementService
from app.BLL.Interfaces.ISchedulePairingService import ISchedulePairingService
from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService
from app.BLL.Interfaces.IRoadmapPairingRequestService import IRoadmapPairingRequestService


from app.BLL.Services.RoleService import RoleService
from app.BLL.Services.UserService import UserService
from app.BLL.Services.PlaceService import PlaceService
from app.BLL.Services.RoutePlaceService import RoutePlaceService
from app.BLL.Services.NotificationService import NotificationService
from app.BLL.Services.ConversationService import ConversationService
from app.BLL.Services.ScheduleManagementService import ScheduleManagementService
from app.BLL.Services.RoadmapShareService import RoadmapShareService
from app.BLL.Services.RoadmapRequestService import RoadmapRequestService
from app.BLL.Services.ScheduleManagementShareRoute import ScheduleManagementShareRoute
from app.BLL.Services.ScheduleShareService import ScheduleShareService
from app.BLL.Services.SchedulePairingManagementService import SchedulePairingManagementService
from app.BLL.Services.SchedulePairingService import SchedulePairingService
from app.BLL.Services.RoadmapPairingService import RoadmapPairingService
from app.BLL.Services.RoadmapPairingRequestService import RoadmapPairingRequestService



from app.lib.lib_ma import UserSchema, RoleSchema, LocationSchema, RouteSchema, PlaceSchema, NotificationSchema, \
                            ConversationSchema, MessageSchema, ScheduleManagementSchema, RoadmapShareSchema, ScheduleShareItemSchema,\
                            CreateRoadmapRequestValidator, RoadmapRequestSchema, UpdateScheduleManagementValidator \
                            , UpdateScheduleShareValidator, SchedulePairingManagementSchema, RoadmapPairingSchema, RoadmapPairingRequestSchema\
                            , LinkNotificationValidator


from injector import Module, singleton, Injector

class TransactionModule(Module):
    def configure(self, binder):
        binder.bind(interface=TransactionManager, to=TransactionManager(session=db.session), scope=singleton)

class RepositoryModule(Module):
    def configure(self, binder):
        binder.bind(interface=IRoleRepository, to=RoleRepository, scope=singleton)
        binder.bind(interface=IUserRepository, to=UserRepository, scope=singleton)
        binder.bind(interface=ILocationRepository, to=LocationRepository, scope=singleton)
        binder.bind(interface=IRouteRepository, to=RouteRepository, scope=singleton)
        binder.bind(interface=IRoutePlaceRepository, to=RoutePlaceRepository, scope=singleton)
        binder.bind(interface=IPlaceRepository, to=PlaceRepository, scope=singleton)
        binder.bind(interface=INotificationRepository, to=NotificationRepository, scope=singleton)
        binder.bind(interface=IConversationRepository, to=ConversationRepository, scope=singleton)
        binder.bind(interface=IScheduleManagementRepository, to=ScheduleManagementRepository, scope=singleton)
        binder.bind(interface=IScheduleShareRepository, to=ScheduleShareRepository, scope=singleton)
        binder.bind(interface=IRoadmapShareRepository, to=RoadmapShareRepository, scope=singleton)
        binder.bind(interface=IRoadmapRequestRepository, to=RoadmapRequestRepository, scope=singleton)
        binder.bind(interface=ISchedulePairingManagementRepository, to=SchedulePairingManagementRepository, scope=singleton)
        binder.bind(interface=ISchedulePairingRepository, to=SchedulePairingRepository, scope=singleton)
        binder.bind(interface=IRoadmapPairingRepository, to=RoadmapPairingRepository, scope=singleton)
        binder.bind(interface=IRoadmapPairingRequestRepository, to=RoadmapPairingRequestRepository, scope=singleton)


class ServiceModule(Module):
    def configure(self, binder):
        binder.bind(interface=IRoleService, to=RoleService, scope=singleton)
        binder.bind(interface=IUserService, to=UserService, scope=singleton)
        binder.bind(interface=IPlaceService, to=PlaceService, scope=singleton)
        binder.bind(interface=IRoutePlaceService, to=RoutePlaceService, scope=singleton)
        binder.bind(interface=INotificationService, to=NotificationService, scope=singleton)
        binder.bind(interface=IConversationService, to=ConversationService, scope=singleton)
        binder.bind(interface=IScheduleManagementService, to=ScheduleManagementService, scope=singleton)
        binder.bind(interface=IRoadmapShareService, to=RoadmapShareService, scope=singleton)
        binder.bind(interface=IRoadmapRequestService, to=RoadmapRequestService, scope=singleton)
        binder.bind(interface=IScheduleShareService, to=ScheduleShareService, scope=singleton)
        binder.bind(interface=ISchedulePairingManagementService, to=SchedulePairingManagementService, scope=singleton)
        binder.bind(interface=ISchedulePairingService, to=SchedulePairingService, scope=singleton)
        binder.bind(interface=IRoadmapPairingService, to=RoadmapPairingService, scope=singleton)
        binder.bind(interface=IScheduleManagementShareRoute, to=ScheduleManagementShareRoute, scope=singleton)
        binder.bind(interface=IRoadmapPairingRequestService, to=RoadmapPairingRequestService, scope=singleton)

            


        
injector = Injector([TransactionModule(), RepositoryModule(), ServiceModule()])




#init schema
role_schema = RoleSchema()
user_schema = UserSchema(only=('user_id', 'user_name', 'user_account', 'roles', 'is_verified', 'status', 'avatar', 'created_time', 'updated_time'))
location_schema = LocationSchema()
schedule_share_item_schema = ScheduleShareItemSchema()
route_schema = RouteSchema()
place_schema = PlaceSchema()
notification_schema = NotificationSchema()
conversation_schema = ConversationSchema()
message_schema = MessageSchema()
schedule_management_schema = ScheduleManagementSchema()
roadmap_share_schema = RoadmapShareSchema()
roadmap_pairing_schema = RoadmapPairingSchema()
schedule_pairing_management_schema = SchedulePairingManagementSchema()
roadmap_pairing_request_schema = RoadmapPairingRequestSchema()
create_roadmap_request_validator = CreateRoadmapRequestValidator()
roadmap_request_schema = RoadmapRequestSchema()
update_schedule_management_schema = UpdateScheduleManagementValidator()
update_schedule_share_schema = UpdateScheduleShareValidator()
link_notification_validator = LinkNotificationValidator()









