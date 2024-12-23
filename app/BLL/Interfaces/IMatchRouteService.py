from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import MatchRoute, User, Route

class IMatchRouteService(ABC):
    @abstractmethod
    def get_list_match_main_user(self, main_user_id: int) -> List[MatchRoute]:
        pass

    @abstractmethod
    def get_list_match_secondary_user(self, secondary_user_id: int) -> List[MatchRoute]:
        pass

    @abstractmethod
    def create_new_match(self, main_user: User, secondary_user: User, route: Route) -> MatchRoute:
        pass

    @abstractmethod
    def get_match_route_by_match_id(self, match_route_id: int) -> MatchRoute:
        pass