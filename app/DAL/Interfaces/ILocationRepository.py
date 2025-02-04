from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Location
from sqlalchemy.orm import Session

class ILocationRepository(ABC):
    @abstractmethod
    def get_locations_all(self, session: Session) -> List[Location]:
        pass
    
    @abstractmethod
    def get_location(self, session: Session, location_id: int) -> Location:
        pass

    @abstractmethod
    def get_location_by_address(self, session: Session, location_address: str) -> Location:
        pass

    @abstractmethod
    def get_locations_by_address(self, session: Session, list_address: List[str]) -> List[Location]:
        pass
    
    @abstractmethod
    def add_location(self, session: Session, location: Location) -> Location:
        pass

    @abstractmethod
    def update_location(self, session: Session, location_id: int) -> Location:
        pass

    @abstractmethod
    def delete_location(self, session: Session, location_id: int) -> bool:
        pass