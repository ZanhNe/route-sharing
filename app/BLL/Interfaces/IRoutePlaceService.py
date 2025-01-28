from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Route, Place

class IRoutePlaceService(ABC):
    @abstractmethod
    def add_place_to_route(self, route: Route, list_places: List[Place]) -> Route:
        pass

    @abstractmethod
    def handle_new_route(self, route_name: str, list_places: List[Place]) -> Route:
        pass

    @abstractmethod
    def get_route_with_place(self, route_name: str, list_place_id: List[str]) -> Route:
        pass

    