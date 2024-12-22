from abc import ABC, abstractmethod
from app.GUI.model.models import Route
from typing import List

class IRouteRepository(ABC):
    @abstractmethod
    def get_routes_all(self) -> List[Route]:
        pass

    @abstractmethod
    def get_route(self, route_id: int) -> Route:
        pass

    @abstractmethod
    def add_route(self, route: Route) -> Route:
        pass

    @abstractmethod
    def update_route(self, route: Route, new_route: Route) -> Route:
        pass

    @abstractmethod
    def delete_route(self, route: Route) -> None:
        pass