from typing import List
from app.GUI.model.models import SchedulePairing
from app.BLL.Interfaces.ISchedulePairingService import ISchedulePairingService
from app.DAL.Interfaces.ISchedulePairingRepository import ISchedulePairingRepository
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class SchedulePairingService(ISchedulePairingService):
    @inject
    def __init__(self, schedule_pairing_repository: ISchedulePairingRepository, tm: TransactionManager):
        self.schedule_pairing_repository = schedule_pairing_repository
        self.tm = tm

    def get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(self, departure_date, schedule_pairing_management_id):
        with self.tm.transaction('Lỗi khi tạo schedule paring') as session:
            schedule_pairing = self.schedule_pairing_repository\
                            .get_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(session=session\
                                                                                                       , departure_date=departure_date\
                                                                                                        , schedule_pairing_management_id=schedule_pairing_management_id)
            if not schedule_pairing:
                schedule_pairing_raw = SchedulePairing(departure_date=departure_date, schedule_pairing_management_id=schedule_pairing_management_id)
                schedule_pairing = self.schedule_pairing_repository.create_schedule_pairing(session=session, schedule_pairing=schedule_pairing_raw)
            return schedule_pairing
        
        
    def update_schedule_pairing(self, schedule_pairing: SchedulePairing) -> SchedulePairing:
        with self.tm.transaction('Lỗi khi cập nhật schedule paring') as session:
            return self.schedule_pairing_repository.update_schedule_pairing(session=session, schedule_pairing=schedule_pairing)
        
        
    def get_or_create_schedule_pairing_by_schedule_pairing_management_id(self, schedule_pairing_management_id):
        pass