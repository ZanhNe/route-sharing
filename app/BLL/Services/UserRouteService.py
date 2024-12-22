from app.GUI.model.models import User, Route
from typing import List
from app.DAL.Interfaces.IUserRouteRepository import IUserRouteRepository
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from app.BLL.Interfaces.IUserRouteService import IUserRouteService

class UserRouteService(IUserRouteService):
    def __init__(self, user_route_repository: IUserRouteRepository, user_repository: IUserRepository, route_repository: IRouteRepository) -> None:
        self.user_route_repository = user_route_repository
        self.user_repository = user_repository
        self.route_repository = route_repository

    def add_route_to_user(self, user: User, route: Route) -> User:
        user_after = self.user_route_repository.add_route_to_user(user=user, route=route)
        if (not user_after):
            return {'error': 'Lỗi trong quá trình thêm tuyến đường cho người dùng'}, 401
        return user_after, 200
    
    def get_user_routes(self, user: User) -> List[Route]:
        pass