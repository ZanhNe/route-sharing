from typing import List
from app.GUI.model.models import Route
from app.BLL.Interfaces.IRouteService import IRouteService
from app.DAL.Interfaces.IRouteRepository import IRouteRepository

class RouteService(IRouteService):
    def __init__(self, route_repository: IRouteRepository) -> None:
        self.route_repository = route_repository

    def get_routes_all(self) -> List[Route]:
        return self.route_repository.get_routes_all(), 200
    
    def get_route(self, route_id: int) -> Route:
        route = self.route_repository.get_route(route_id=route_id)
        if (not route):
            return {'error': 'Route not found'}, 404
        return route, 200
    
    def add_route(self, route: Route) -> Route:
        add_route = self.route_repository.add_route(route=route)
        if (not add_route):
            return {'error': 'Lỗi khi thêm tuyến đường'}, 400
        return add_route, 200
    
    def update_route(self, route: Route, new_route: Route) -> Route:
        route = self.route_repository.update_route(route=route, new_route=new_route)
        if (not route):
            return {'error': 'Lỗi khi sửa đối tượng tuyến đường'}, 400
        return route, 200

    def delete_route(self, route: Route) -> None:
        flag = self.route_repository.delete_route(route=route)
        if (not flag):
            return {'error': 'Lỗi không xác định khi xóa'}, 400
        return {'success': 'Xóa thành công'}, 200