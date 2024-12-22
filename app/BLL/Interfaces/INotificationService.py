from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Notification, User

class INotificationService(ABC):    
    @abstractmethod
    def get_all_notifications_of_user(self, user_id: int) -> List[Notification]:
        pass

    @abstractmethod
    def add_new_notification_of_user(self, noti_type: str, content: str, main_user: User, secondary_user: User) -> Notification:
        pass
    
