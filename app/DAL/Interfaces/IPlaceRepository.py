from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Place, Location
from sqlalchemy.orm import Session

class IPlaceRepository(ABC):
    
    @abstractmethod
    def get_place(self, session: Session, place_id: str) -> Place:
        pass

    @abstractmethod
    def get_places_by_list_id(self, session: Session, list_place_id: List[str]) -> List[Place]:
        pass

    @abstractmethod
    def create_place(self, session: Session, place: Place, location: Location) -> Place:
        pass

    @abstractmethod
    def get_places_by_list_id_include_null(self, session: Session, list_place_id: List[str]) -> List[Place]:
        pass
    
