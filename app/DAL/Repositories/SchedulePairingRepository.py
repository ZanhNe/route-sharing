from typing import List
from app.GUI.model.models import SchedulePairing
from app.DAL.Interfaces.ISchedulePairingRepository import ISchedulePairingRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class SchedulePairingRepository(ISchedulePairingRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_schedule_pairing_by_schedule_pairing_management_id(self, schedule_pairing_management_id):
        return self.session.query(SchedulePairing).filter(SchedulePairing.schedule_pairing_management_id == schedule_pairing_management_id).first()
    
    def get_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(self, departure_date, schedule_pairing_management_id):
        return self.session.query(SchedulePairing).filter(SchedulePairing.departure_date == departure_date, SchedulePairing.schedule_pairing_management_id == schedule_pairing_management_id).first()


    def create_schedule_pairing(self, schedule_pairing):
        try:
            self.session.add(instance=schedule_pairing)
            self.session.commit()
            return schedule_pairing
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise Exception('Lỗi khi tạo lịch trình ghép cặp')
        
    def update_schedule_pairing(self, schedule_pairing: SchedulePairing) -> SchedulePairing:
        try:
            self.session.add(schedule_pairing)
            self.session.commit()
            return schedule_pairing
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise Exception('Lỗi khi cập nhật lịch trình ghép cặp')
        