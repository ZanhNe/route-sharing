from app.DAL.Interfaces.INotificationRepository import INotificationRepository
from typing import List
from app.GUI.model.models import Notification, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class NotificationRepository(INotificationRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_all_notifications_of_user(self, user_id) -> List[Notification]:
        return self.session.query(Notification).join(User, User.user_id == Notification.main_user_id).filter(User.user_id == user_id).order_by(Notification.notification_id.desc()).all()
    
    def add_new_notification_of_user(self, noti_type, content, main_user, secondary_user) -> Notification:
        try:
            notification = Notification(noti_type=noti_type, content=content, main_user=main_user, secondary_user=secondary_user)
            self.session.add(notification)
            self.session.commit()
            return notification
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
        
