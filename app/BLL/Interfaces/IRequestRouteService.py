# from abc import ABC, abstractmethod
# from typing import List
# from app.GUI.model.models import RequestRoute, User, Route

# class IRequestRouteService(ABC):

#     @abstractmethod
#     def create_request_route(self, main_user: User, secondary_user: User, route: Route) -> RequestRoute:
#         pass

#     @abstractmethod
#     def get_request_by_request_id(self, request_id: int) -> RequestRoute:
#         pass

#     @abstractmethod
#     def get_requests_route_main_user_pending(self, main_user_id: str) -> List[RequestRoute]:
#         pass

#     @abstractmethod
#     def get_requests_route_secondary_user_pending(self, secondary_user_id: str) -> List[RequestRoute]:
#         pass

#     @abstractmethod
#     def get_requests_by_list_request_id(self, list_request_id: List[int]) -> List[RequestRoute]:
#         pass

#     @abstractmethod
#     def get_requests_route_main_user(self, main_user_id: str) -> List[RequestRoute]:
#         pass

#     @abstractmethod
#     def update_status_request_route(self, status: str, request_route: RequestRoute) -> RequestRoute:
#         pass