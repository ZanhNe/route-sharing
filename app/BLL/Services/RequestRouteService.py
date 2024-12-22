from app.GUI.model.models import RequestRoute, User, Route
from typing import List
from app.BLL.Interfaces.IRequestRouteService import IRequestRouteService
from app.DAL.Interfaces.IRequestRouteRepository import IRequestRouteRepository

class RequestRouteService(IRequestRouteService):
    def __init__(self, request_route_repository: IRequestRouteRepository):
        self.request_route_repository = request_route_repository

    def get_requests_route_main_user(self, main_user_id: int) -> RequestRoute:
        return self.request_route_repository.get_requests_route(main_user_id=main_user_id)
    
    def get_request_by_request_id(self, request_id: int):
        return self.request_route_repository.get_request_by_request_id(request_id=request_id)
    
    def get_requests_route_main_user_pending(self, main_user_id: int) -> List[RequestRoute]:
        return self.request_route_repository.get_requests_route_main_user_pending(main_user_id=main_user_id)
    
    def get_requests_route_secondary_user_pending(self, secondary_user_id: int) -> List[RequestRoute]:
        return self.request_route_repository.get_requests_route_secondary_user_pending(secondary_user_id=secondary_user_id)

    def create_request_route(self, main_user: User, secondary_user: User, route: Route) -> RequestRoute:
        return self.request_route_repository.create_request_route(main_user=main_user, secondary_user=secondary_user, route=route)
    

    def get_requests_by_list_request_id(self, list_request_id: List[int]) -> List[RequestRoute]:
        return self.request_route_repository.get_requests_by_list_request_id(list_request_id=list_request_id)

    def update_status_request_route(self, status: str, request_route: RequestRoute) -> RequestRoute:
        return self.request_route_repository.update_status_request_route(status=status, request_route=request_route)
    
    def update_status_accept_request(self, main_user_id: int, request_id: int):
        self.request_route_repository.update_status_accept_request(main_user_id=main_user_id, request_id=request_id)
    
    
