from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Place, Location

class IPlaceRepository(ABC):
    
    @abstractmethod
    def get_place(self, place_id: str) -> Place:
        pass

    @abstractmethod
    def get_places_by_list_id(self, list_place_id: List[str]) -> List[Place]:
        pass

    @abstractmethod
    def create_place(self, place: Place, location: Location) -> Place:
        pass

    @abstractmethod
    def get_places_by_list_id_include_null(self, list_place_id: List[str]) -> List[Place]:
        pass
    
