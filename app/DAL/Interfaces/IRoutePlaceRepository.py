from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Place, Route

class IRoutePlaceRepository(ABC):
    @abstractmethod
    def add_place_to_route(self, route: Route, list_places: List[Place]) -> Route:
        pass

    