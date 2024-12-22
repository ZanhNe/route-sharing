from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Location

class ILocationRepository(ABC):
    @abstractmethod
    def get_locations_all(self) -> List[Location]:
        pass
    
    @abstractmethod
    def get_location(self, location_id: int) -> Location:
        pass

    @abstractmethod
    def get_location_by_address(self, location_address: str) -> Location:
        pass

    @abstractmethod
    def get_locations_by_address(self, list_address: List[str]) -> List[Location]:
        pass
    
    @abstractmethod
    def add_location(self, location: Location) -> Location:
        pass

    @abstractmethod
    def update_location(self, location_id: int) -> Location:
        pass

    @abstractmethod
    def delete_location(self, location_id: int) -> bool:
        pass