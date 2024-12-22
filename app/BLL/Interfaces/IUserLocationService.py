from app.GUI.model.models import Location, User
from abc import ABC, abstractmethod

class IUserLocationService(ABC):
    @abstractmethod
    def add_location_user(self, user: User, location: Location) -> Location:
        pass