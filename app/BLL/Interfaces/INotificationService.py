from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Notification, User

class INotificationService(ABC):    
    @abstractmethod
    def get_all_notifications_of_user(self, user_id: str) -> List[Notification]:
        pass

    @abstractmethod
    def add_new_notification_request_roadmap_of_user(self, validator: dict) -> Notification:
        pass
    
