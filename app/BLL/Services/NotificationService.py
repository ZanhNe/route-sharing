from app.GUI.model.models import Notification, User
from typing import List
from app.BLL.Interfaces.INotificationService import INotificationService
from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class NotificationService(INotificationService):

    @inject
    def __init__(self, notification_repository: INotificationRepository, tm: TransactionManager):
        self.notification_repository = notification_repository
        self.tm = tm

    def get_all_notifications_of_user(self, user_id: str) -> List[Notification]:
        with self.tm.transaction('') as session:
            return self.notification_repository.get_all_notifications_of_user(session=session, user_id=user_id)
    
    def add_new_notification_request_roadmap_of_user(self, validator: dict) -> Notification:
        with self.tm.transaction('Lỗi khi thêm notification cho request roadmap') as session:
            notification = Notification(content='Một người muốn ghép cặp lộ trình với bạn', main_user_id=validator['receiver_id'], secondary_user_id=validator['sender_id'])
            return self.notification_repository.add_new_notification_of_user(session=session, notification=notification)
        
    
            
    
    def add_new_notification_status_request(self, validator: dict) -> Notification:
        with self.tm.transaction('Lỗi khi thêm notification cho request status') as session:
            notification = Notification(content=validator['content'], main_user_id=validator['receiver_id'], secondary_user_id=validator['sender_id'])
            return self.notification_repository.add_new_notification_of_user(session=session, notification=notification)
        

