from app.GUI.model.models import db
from app.custom.Helper.Helper import TransactionManager
from .DIContainer import RepositoryDIContainer, ServiceDIContainer
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.ILocationRepository import ILocationRepository
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from app.DAL.Interfaces.IUserRoleRepository import IUserRoleRepository
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




from app.DAL.Repositories.RoleRepository import RoleRepository
from app.DAL.Repositories.UserRepository import UserRepository
from app.DAL.Repositories.LocationRepository import LocationRepository
from app.DAL.Repositories.RouteRepository import RouteRepository
from app.DAL.Repositories.UserRoleRepository import UserRoleRepository
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


from app.BLL.Interfaces.IRoleService import IRoleService
from app.BLL.Interfaces.IUserService import IUserService
from app.BLL.Interfaces.ILocationService import ILocationService
from app.BLL.Interfaces.IRouteService import IRouteService
from app.BLL.Interfaces.IUserRoleService import IUserRoleService
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


from app.BLL.Services.RoleService import RoleService
from app.BLL.Services.UserService import UserService
from app.BLL.Services.LocationService import LocationService
from app.BLL.Services.RouteService import RouteService
from app.BLL.Services.PlaceService import PlaceService

from app.BLL.Services.UserRoleService import UserRoleService
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



from app.lib.lib_ma import UserSchema, RoleSchema, LocationSchema, RouteSchema, PlaceSchema, NotificationSchema, \
                            ConversationSchema, MessageSchema, ScheduleManagementSchema, RoadmapShareSchema, ScheduleShareItemSchema, \
                            CreateRoadmapRequestValidator, RoadmapRequestSchema, UpdateScheduleManagementValidator \
                            , UpdateScheduleShareValidator


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
        binder.bind(interface=IUserRoleRepository, to=UserRoleRepository, scope=singleton)
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

class ServiceModule(Module):
    def configure(self, binder):
        binder.bind(interface=IRoleService, to=RoleService, scope=singleton)
        binder.bind(interface=IUserService, to=UserService, scope=singleton)
        binder.bind(interface=ILocationService, to=LocationService, scope=singleton)
        binder.bind(interface=IRouteService, to=RouteService, scope=singleton)
        binder.bind(interface=IUserRoleService, to=UserRoleService, scope=singleton)
        binder.bind(interface=IRoutePlaceService, to=RoutePlaceService, scope=singleton)
        binder.bind(interface=INotificationService, to=NotificationService, scope=singleton)
        binder.bind(interface=IConversationService, to=ConversationService, scope=singleton)
        binder.bind(interface=IScheduleManagementService, to=ScheduleManagementService, scope=singleton)
        binder.bind(interface=IRoadmapShareService, to=RoadmapShareService, scope=singleton)
        binder.bind(interface=IRoadmapRequestService, to=RoadmapRequestService, scope=singleton)
        binder.bind(interface=IScheduleShareService, to=ScheduleShareService, scope=singleton)
        binder.bind(interface=IScheduleManagementShareRoute, to=ScheduleManagementShareRoute, scope=singleton)
        binder.bind(interface=ISchedulePairingManagementService, to=SchedulePairingManagementService, scope=singleton)
        binder.bind(interface=ISchedulePairingService, to=SchedulePairingService, scope=singleton)
        binder.bind(interface=IRoadmapPairingService, to=RoadmapPairingService, scope=singleton)

            

        


        
injector = Injector([RepositoryModule(), ServiceModule()])

#initial
repository_factory = RepositoryDIContainer()
service_factory = ServiceDIContainer()

#register (dependency injection)
repository_factory.register_container(IRoleRepository, RoleRepository)
repository_factory.register_container(IUserRepository, UserRepository)
repository_factory.register_container(ILocationRepository, LocationRepository)
repository_factory.register_container(IRouteRepository, RouteRepository)
repository_factory.register_container(IUserRoleRepository, UserRoleRepository)
repository_factory.register_container(IRoutePlaceRepository, RoutePlaceRepository)
repository_factory.register_container(IPlaceRepository, PlaceRepository)
repository_factory.register_container(INotificationRepository, NotificationRepository)
repository_factory.register_container(IConversationRepository, ConversationRepository)
repository_factory.register_container(IScheduleManagementRepository, ScheduleManagementRepository)
repository_factory.register_container(IScheduleShareRepository, ScheduleShareRepository)
repository_factory.register_container(IRoadmapShareRepository, RoadmapShareRepository)
repository_factory.register_container(IRoadmapRequestRepository, RoadmapRequestRepository)
repository_factory.register_container(ISchedulePairingManagementRepository, SchedulePairingManagementRepository)
repository_factory.register_container(ISchedulePairingRepository, SchedulePairingRepository)
repository_factory.register_container(IRoadmapPairingRepository, RoadmapPairingRepository)



service_factory.register_container(IRoleService, RoleService)
service_factory.register_container(IUserService, UserService)
service_factory.register_container(ILocationService, LocationService)
service_factory.register_container(IRouteService, RouteService)
service_factory.register_container(IPlaceService, PlaceService)
service_factory.register_container(IUserRoleService, UserRoleService)
service_factory.register_container(IRoutePlaceService, RoutePlaceService)
service_factory.register_container(INotificationService, NotificationService)
service_factory.register_container(IConversationService, ConversationService)
service_factory.register_container(IScheduleManagementService, ScheduleManagementService)
service_factory.register_container(IRoadmapShareService, RoadmapShareService)
service_factory.register_container(IRoadmapRequestService, RoadmapRequestService) 
service_factory.register_container(IScheduleShareService, ScheduleShareService) 

service_factory.register_container(IScheduleManagementShareRoute, ScheduleManagementShareRoute)
service_factory.register_container(ISchedulePairingManagementService, SchedulePairingManagementService)
service_factory.register_container(ISchedulePairingService, SchedulePairingService)
service_factory.register_container(IRoadmapPairingService, RoadmapPairingService)




#get instance 
role_repository = repository_factory.resolve(IRoleRepository)()
user_repository = repository_factory.resolve(IUserRepository)()
location_repository = repository_factory.resolve(ILocationRepository)()
route_repository = repository_factory.resolve(IRouteRepository)()
user_role_repository = repository_factory.resolve(IUserRoleRepository)()
route_place_repository = repository_factory.resolve(IRoutePlaceRepository)()
place_repository = repository_factory.resolve(IPlaceRepository)()
notification_repository = repository_factory.resolve(INotificationRepository)()
conversation_repository = repository_factory.resolve(IConversationRepository)()
schedule_management_repository = repository_factory.resolve(IScheduleManagementRepository)()
schedule_share_repository = repository_factory.resolve(IScheduleShareRepository)()
roadmap_share_repository = repository_factory.resolve(IRoadmapShareRepository)()
roadmap_request_repository = repository_factory.resolve(IRoadmapRequestRepository)()

schedule_pairing_management_repository = repository_factory.resolve(ISchedulePairingManagementRepository)()
schedule_pairing_repository = repository_factory.resolve(ISchedulePairingRepository)()
roadmap_pairing_repository = repository_factory.resolve(IRoadmapPairingRepository)()


role_service = service_factory.resolve(IRoleService)(role_repository)
user_service = service_factory.resolve(IUserService)(user_repository, role_repository)
location_service = service_factory.resolve(ILocationService)(location_repository)
route_service = service_factory.resolve(IRouteService)(route_repository)
user_role_service = service_factory.resolve(IUserRoleService)(user_role_repository)
route_place_service = service_factory.resolve(IRoutePlaceService)(route_place_repository=route_place_repository, place_repository=place_repository, route_repository=route_repository)
place_service = service_factory.resolve(IPlaceService)(place_repository)
notification_service = service_factory.resolve(INotificationService)(notification_repository)
conversation_service = service_factory.resolve(IConversationService)(conversation_repository)
schedule_management_service = service_factory.resolve(IScheduleManagementService)(schedule_management_repository, schedule_share_repository)
schedule_share_service = service_factory.resolve(IScheduleShareService)(schedule_share_repository)
roadmap_share_service = service_factory.resolve(IRoadmapShareService)(roadmap_share_repository)
roadmap_request_service = service_factory.resolve(IRoadmapRequestService)(roadmap_request_repository)

schedule_pairing_management_service = service_factory.resolve(ISchedulePairingManagementService)(schedule_pairing_management_repository)
schedule_pairing_service = service_factory.resolve(ISchedulePairingService)(schedule_pairing_repository)
roadmap_pairing_service = service_factory.resolve(IRoadmapPairingService)(roadmap_pairing_repository)

schedule_management_share_route = service_factory\
                                    .resolve(IScheduleManagementShareRoute)(schedule_management_service\
                                                    , route_place_service, notification_service\
                                                    , roadmap_request_service, schedule_share_service, roadmap_share_service\
                                                    , schedule_pairing_management_service, schedule_pairing_service, roadmap_pairing_service)




#init schema
role_schema = RoleSchema()
user_schema = UserSchema(only=('user_id', 'user_name', 'user_account', 'roles', 'status', 'avatar', 'created_time', 'updated_time'))
location_schema = LocationSchema()
schedule_share_item_schema = ScheduleShareItemSchema()
route_schema = RouteSchema()
place_schema = PlaceSchema()
notification_schema = NotificationSchema()
conversation_schema = ConversationSchema()
message_schema = MessageSchema()
schedule_management_schema = ScheduleManagementSchema()
roadmap_share_schema = RoadmapShareSchema()
create_roadmap_request_validator = CreateRoadmapRequestValidator()
roadmap_request_schema = RoadmapRequestSchema()
update_schedule_management_schema = UpdateScheduleManagementValidator()
update_schedule_share_schema = UpdateScheduleShareValidator()









