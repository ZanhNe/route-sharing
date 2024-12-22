from abc import ABC, abstractmethod
from app.GUI.model.models import UserRouteShare, User, Route
from typing import List

class IRouteShareRepository(ABC):
    
    @abstractmethod
    def get_route_share(self, route_share_id: int) -> UserRouteShare:
        pass
    
    @abstractmethod
    def get_all_routes_share(self) -> List[UserRouteShare]:
        pass

    @abstractmethod
    def get_all_routes_share_is_not_match(self) -> List[UserRouteShare]:
        pass
    
    @abstractmethod
    def add_route_share(self, route_share: UserRouteShare, user: User, route: Route) -> UserRouteShare:
        pass

