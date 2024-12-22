from app.GUI.model.models import db
from .DIContainer import RepositoryDIContainer, ServiceDIContainer
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.ILocationRepository import ILocationRepository
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from app.DAL.Interfaces.IUserLocationRepository import IUserLocationRepository
from app.DAL.Interfaces.IUserRoleRepository import IUserRoleRepository
from app.DAL.Interfaces.IRoutePlaceRepository import IRoutePlaceRepository
from app.DAL.Interfaces.IUserRouteRepository import IUserRouteRepository
from app.DAL.Interfaces.IPlaceRepository import IPlaceRepository
from app.DAL.Interfaces.IRouteShareRepository import IRouteShareRepository
from app.DAL.Interfaces.IRequestRouteRepository import IRequestRouteRepository
from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from app.DAL.Interfaces.IMatchRouteRepository import IMatchRouteRepository
from app.DAL.Interfaces.IConversationRepository import IConversationRepository


from app.DAL.Repositories.RoleRepository import RoleRepository
from app.DAL.Repositories.UserRepository import UserRepository
from app.DAL.Repositories.LocationRepository import LocationRepository
from app.DAL.Repositories.RouteRepository import RouteRepository
from app.DAL.Repositories.UserLocationRepository import UserLocationRepository
from app.DAL.Repositories.UserRoleRepository import UserRoleRepository
from app.DAL.Repositories.RoutePlaceRepository import RoutePlaceRepository
from app.DAL.Repositories.UserRouteRepository import UserRouteRepository
from app.DAL.Repositories.PlaceRepository import PlaceRepository
from app.DAL.Repositories.RouteShareRepository import RouteShareRepository
from app.DAL.Repositories.RequestRouteRepository import RequestRouteRepository
from app.DAL.Repositories.NotificationRepository import NotificationRepository
from app.DAL.Repositories.MatchRouteRepository import MatchRouteRepository
from app.DAL.Repositories.ConversationRepository import ConversationRepository


from app.BLL.Interfaces.IRoleService import IRoleService
from app.BLL.Interfaces.IUserService import IUserService
from app.BLL.Interfaces.ILocationService import ILocationService
from app.BLL.Interfaces.IRouteService import IRouteService
from app.BLL.Interfaces.IUserLocationService import IUserLocationService
from app.BLL.Interfaces.IUserRoleService import IUserRoleService
from app.BLL.Interfaces.IRoutePlaceService import IRoutePlaceService
from app.BLL.Interfaces.IUserRouteService import IUserRouteService
from app.BLL.Interfaces.IPlaceService import IPlaceService
from app.BLL.Interfaces.IRouteShareService import IRouteShareService
from app.BLL.Interfaces.IRequestRouteService import IRequestRouteService
from app.BLL.Interfaces.INotificationService import INotificationService
from app.BLL.Interfaces.IMatchRouteService import IMatchRouteService
from app.BLL.Interfaces.IConversationService import IConversationService


from app.BLL.Services.RoleService import RoleService
from app.BLL.Services.UserService import UserService
from app.BLL.Services.LocationService import LocationService
from app.BLL.Services.RouteService import RouteService
from app.BLL.Services.UserLocationService import UserLocationService
from app.BLL.Services.UserRoleService import UserRoleService
from app.BLL.Services.RoutePlaceService import RoutePlaceService
from app.BLL.Services.UserRouteService import UserRouteService
from app.BLL.Services.PlaceService import PlaceService
from app.BLL.Services.RouteShareService import RouteShareService
from app.BLL.Services.RequestRouteService import RequestRouteService
from app.BLL.Services.NotificationService import NotificationService
from app.BLL.Services.MatchRouteService import MatchRouteService
from app.BLL.Services.ConversationService import ConversationService



from app.lib.lib_ma import UserSchema, RoleSchema, LocationSchema, RouteSchema, PlaceSchema, UserRouteShareSchema, RequestRouteSchema, NotificationSchema, MatchRouteSchema, ConversationSchema, MessageSchema



#initial
repository_factory = RepositoryDIContainer()
service_factory = ServiceDIContainer()

#register (dependency injection)
repository_factory.register_container(IRoleRepository, RoleRepository)
repository_factory.register_container(IUserRepository, UserRepository)
repository_factory.register_container(ILocationRepository, LocationRepository)
repository_factory.register_container(IRouteRepository, RouteRepository)
repository_factory.register_container(IUserLocationRepository, UserLocationRepository)
repository_factory.register_container(IUserRoleRepository, UserRoleRepository)
repository_factory.register_container(IRoutePlaceRepository, RoutePlaceRepository)
repository_factory.register_container(IUserRouteRepository, UserRouteRepository)
repository_factory.register_container(IPlaceRepository, PlaceRepository)
repository_factory.register_container(IRouteShareRepository, RouteShareRepository)
repository_factory.register_container(IRequestRouteRepository, RequestRouteRepository)
repository_factory.register_container(INotificationRepository, NotificationRepository)
repository_factory.register_container(IMatchRouteRepository, MatchRouteRepository)
repository_factory.register_container(IConversationRepository, ConversationRepository)



service_factory.register_container(IRoleService, RoleService)
service_factory.register_container(IUserService, UserService)
service_factory.register_container(ILocationService, LocationService)
service_factory.register_container(IRouteService, RouteService)
service_factory.register_container(IUserLocationService, UserLocationService)
service_factory.register_container(IUserRoleService, UserRoleService)
service_factory.register_container(IRoutePlaceService, RoutePlaceService)
service_factory.register_container(IUserRouteService, UserRouteService)
service_factory.register_container(IPlaceService, PlaceService)
service_factory.register_container(IRouteShareService, RouteShareService)
service_factory.register_container(IRequestRouteService, RequestRouteService)
service_factory.register_container(INotificationService, NotificationService)
service_factory.register_container(IMatchRouteService, MatchRouteService)
service_factory.register_container(IConversationService, ConversationService)





#get instance 
role_repository = repository_factory.resolve(IRoleRepository)(session=db.session)
user_repository = repository_factory.resolve(IUserRepository)(session=db.session)
location_repository = repository_factory.resolve(ILocationRepository)(session=db.session)
route_repository = repository_factory.resolve(IRouteRepository)(session=db.session)
user_location_repository = repository_factory.resolve(IUserLocationRepository)(session=db.session)
user_role_repository = repository_factory.resolve(IUserRoleRepository)(session=db.session)
route_place_repository = repository_factory.resolve(IRoutePlaceRepository)(session=db.session)
user_route_repository = repository_factory.resolve(IUserRouteRepository)(session=db.session)
place_repository = repository_factory.resolve(IPlaceRepository)(session=db.session)
route_share_repository = repository_factory.resolve(IRouteShareRepository)(session=db.session)
request_route_repository = repository_factory.resolve(IRequestRouteRepository)(session=db.session)
notification_repository = repository_factory.resolve(INotificationRepository)(session=db.session)
match_route_repository = repository_factory.resolve(IMatchRouteRepository)(session=db.session)
conversation_repository = repository_factory.resolve(IConversationRepository)(session=db.session)


role_service = service_factory.resolve(IRoleService)(role_repository)
user_service = service_factory.resolve(IUserService)(user_repository)
location_service = service_factory.resolve(ILocationService)(location_repository)
route_service = service_factory.resolve(IRouteService)(route_repository)
user_location_service = service_factory.resolve(IUserLocationService)(user_location_repository)
user_role_service = service_factory.resolve(IUserRoleService)(user_role_repository)
route_place_service = service_factory.resolve(IRoutePlaceService)(route_place_repository=route_place_repository, place_repository=place_repository, route_repository=route_repository)
user_route_service = service_factory.resolve(IUserRouteService)(user_route_repository=user_route_repository, user_repository=user_repository, route_repository=route_repository)
place_service = service_factory.resolve(IPlaceService)(place_repository)
route_share_service = service_factory.resolve(IRouteShareService)(route_share_repository)
request_route_service = service_factory.resolve(IRequestRouteService)(request_route_repository)
notification_service = service_factory.resolve(INotificationService)(notification_repository)
match_route_service = service_factory.resolve(IMatchRouteService)(match_route_repository)
conversation_service = service_factory.resolve(IConversationService)(conversation_repository)



#init schema
role_schema = RoleSchema()
user_schema = UserSchema(only=('user_id', 'user_name', 'roles', 'status', 'avatar'))
location_schema = LocationSchema()
route_schema = RouteSchema()
place_schema = PlaceSchema()
route_share_schema = UserRouteShareSchema()
request_route_schema = RequestRouteSchema()
notification_schema = NotificationSchema()
match_route_schema = MatchRouteSchema()
conversation_schema = ConversationSchema()
message_schema = MessageSchema()






