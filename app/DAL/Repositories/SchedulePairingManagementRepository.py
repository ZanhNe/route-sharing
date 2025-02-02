from typing import List
from app.GUI.model.models import SchedulePairingManagement
from app.DAL.Interfaces.ISchedulePairingManagementRepository import ISchedulePairingManagementRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class SchedulePairingManagementRepository(ISchedulePairingManagementRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_schedule_pairing_management_of_user(self, user_id):
        return self.session.query(SchedulePairingManagement).filter(SchedulePairingManagement.user_id == user_id).first()
    
    def create_schedule_pairing_management_of_user(self, schedule_pairing_management):
        try:
            self.session.add(instance=schedule_pairing_management)
            self.session.commit()
            return schedule_pairing_management
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise Exception('Lỗi khi tạo quản lý lịch trình ghép cặp')