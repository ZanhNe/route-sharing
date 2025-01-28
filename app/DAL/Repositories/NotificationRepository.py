from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from typing import List
from app.GUI.model.models import Notification, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class NotificationRepository(INotificationRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_notifications_of_user(self, user_id) -> List[Notification]:
        return self.session.query(Notification).filter(Notification.main_user_id == user_id).order_by(Notification.notification_id.desc()).all()
    
    def add_new_notification_of_user(self, notification: Notification) -> Notification:
        try:
            self.session.add(notification)
            self.session.commit()
            return notification
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise e
        
