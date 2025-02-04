from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Notification, User
from sqlalchemy.orm import Session


class INotificationRepository(ABC):

    @abstractmethod
    def get_all_notifications_of_user(self, session: Session, user_id: str) -> List[Notification]:
        pass

    @abstractmethod
    def add_new_notification_of_user(self, session: Session, notification: Notification) -> Notification:
        pass
    
