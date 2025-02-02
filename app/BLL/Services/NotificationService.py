from app.GUI.model.models import Notification, User
from typing import List
from app.BLL.Interfaces.INotificationService import INotificationService
from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from sqlalchemy.exc import SQLAlchemyError

class NotificationService(INotificationService):

    def __init__(self, notification_repository: INotificationRepository):
        self.notification_repository = notification_repository

    def get_all_notifications_of_user(self, user_id: str) -> List[Notification]:
        return self.notification_repository.get_all_notifications_of_user(user_id=user_id)
    
    def add_new_notification_request_roadmap_of_user(self, validator: dict) -> Notification:
        try:
            notification = Notification(content='Một người muốn ghép cặp lộ trình với bạn', main_user_id=validator['receiver_id'], secondary_user_id=validator['sender_id'])
            return self.notification_repository.add_new_notification_of_user(notification=notification)
        except SQLAlchemyError as e:
            raise e
        
    def add_new_notification_status_request(self, validator: dict) -> Notification:
        try:
            notification = Notification(content=validator['content'], main_user_id=validator['receiver_id'], secondary_user_id=validator['sender_id'])
            return self.notification_repository.add_new_notification_of_user(notification=notification)
        except SQLAlchemyError as e:
            raise e

