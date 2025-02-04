from typing import List
from app.GUI.model.models import SchedulePairingManagement
from app.DAL.Interfaces.ISchedulePairingManagementRepository import ISchedulePairingManagementRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class SchedulePairingManagementRepository(ISchedulePairingManagementRepository):


    def get_schedule_pairing_management_of_user(self, session: Session, user_id):
        return session.query(SchedulePairingManagement).filter(SchedulePairingManagement.user_id == user_id).first()
    
    def create_schedule_pairing_management_of_user(self, session: Session, schedule_pairing_management):
        session.add(instance=schedule_pairing_management)
        return schedule_pairing_management
