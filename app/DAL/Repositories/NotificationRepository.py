from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from typing import List
from app.GUI.model.models import Notification, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class NotificationRepository(INotificationRepository):

    
    def get_all_notifications_of_user(self, session: Session, user_id) -> List[Notification]:
        return session.query(Notification).filter(Notification.main_user_id == user_id).order_by(Notification.notification_id.desc()).all()
    
    def add_new_notification_of_user(self, session: Session, notification: Notification) -> Notification:
        session.add(notification)
        return notification

        
