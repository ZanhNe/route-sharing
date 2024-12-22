from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import User, Route

class IUserRouteRepository(ABC):
    @abstractmethod
    def add_route_to_user(self, user: User, route: Route) -> User:
        pass

    @abstractmethod
    def get_user_routes(self, user: User) -> List[Route]:
        pass