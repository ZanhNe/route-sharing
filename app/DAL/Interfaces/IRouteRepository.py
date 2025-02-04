from abc import ABC, abstractmethod
from app.GUI.model.models import Route
from typing import List
from sqlalchemy.orm import Session

class IRouteRepository(ABC):
    @abstractmethod
    def get_routes_all(self, session: Session) -> List[Route]:
        pass

    @abstractmethod
    def get_routes_by_list_places_id(self, session: Session, list_places_id) -> List[Route]:
        pass

    @abstractmethod
    def get_route(self, session: Session, route_id: int) -> Route:
        pass

    @abstractmethod
    def add_route(self, session: Session, route: Route) -> Route:
        pass

    @abstractmethod
    def update_route(self, session: Session, route: Route, new_route: Route) -> Route:
        pass

    @abstractmethod
    def delete_route(self, session: Session, route: Route) -> None:
        pass