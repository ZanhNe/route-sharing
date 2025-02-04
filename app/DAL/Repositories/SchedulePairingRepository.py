from typing import List
from app.GUI.model.models import SchedulePairing
from app.DAL.Interfaces.ISchedulePairingRepository import ISchedulePairingRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class SchedulePairingRepository(ISchedulePairingRepository):

    def get_schedule_pairing_by_schedule_pairing_management_id(self, session: Session, schedule_pairing_management_id):
        return session.query(SchedulePairing).filter(SchedulePairing.schedule_pairing_management_id == schedule_pairing_management_id).first()
    
    def get_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(self, session: Session, departure_date, schedule_pairing_management_id):
        return session.query(SchedulePairing).filter(SchedulePairing.departure_date == departure_date, SchedulePairing.schedule_pairing_management_id == schedule_pairing_management_id).first()


    def create_schedule_pairing(self, session: Session, schedule_pairing):
        session.add(instance=schedule_pairing)
        return schedule_pairing
        
    def update_schedule_pairing(self, session: Session, schedule_pairing: SchedulePairing) -> SchedulePairing:
        session.add(schedule_pairing)
        return schedule_pairing
        