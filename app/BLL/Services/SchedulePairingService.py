from typing import List
from app.GUI.model.models import SchedulePairing
from app.BLL.Interfaces.ISchedulePairingService import ISchedulePairingService
from app.DAL.Interfaces.ISchedulePairingRepository import ISchedulePairingRepository

class SchedulePairingService(ISchedulePairingService):
    def __init__(self, schedule_pairing_repository: ISchedulePairingRepository):
        self.schedule_pairing_repository = schedule_pairing_repository

    def get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(self, departure_date, schedule_pairing_management_id):
        try:
            schedule_pairing = self.schedule_pairing_repository\
                            .get_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(departure_date=departure_date, schedule_pairing_management_id=schedule_pairing_management_id)
            if not schedule_pairing:
                schedule_pairing_raw = SchedulePairing(departure_date=departure_date, schedule_pairing_management_id=schedule_pairing_management_id)
                schedule_pairing = self.schedule_pairing_repository.create_schedule_pairing(schedule_pairing=schedule_pairing_raw)
            return schedule_pairing
        except Exception as e:
            raise e
        
    def update_schedule_pairing(self, schedule_pairing: SchedulePairing) -> SchedulePairing:
        try:
            return self.schedule_pairing_repository.update_schedule_pairing(schedule_pairing=schedule_pairing)
        except Exception as e:
            raise e
        
    def get_or_create_schedule_pairing_by_schedule_pairing_management_id(self, schedule_pairing_management_id):
        pass