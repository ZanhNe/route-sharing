from abc import ABC, abstractmethod
from app.GUI.model.models import Location, User
from typing import List

class IUserLocationRepository(ABC):
    @abstractmethod
    def add_location_user(self, user: User, location: Location) -> Location:
        pass
    