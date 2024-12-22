from app.GUI.model.models import Notification, User
from typing import List
from app.BLL.Interfaces.INotificationService import INotificationService
from app.DAL.Interfaces.INotificationRepository import INotificationRepository

class NotificationService(INotificationService):

    def __init__(self, notification_repository: INotificationRepository):
        self.notification_repository = notification_repository

    def get_all_notifications_of_user(self, user_id: int) -> List[Notification]:
        return self.notification_repository.get_all_notifications_of_user(user_id=user_id)
    
    def add_new_notification_of_user(self, noti_type: str, content: str, main_user: User, secondary_user: User) -> Notification:
        return self.notification_repository.add_new_notification_of_user(content=content, noti_type=noti_type, main_user=main_user, secondary_user=secondary_user)

