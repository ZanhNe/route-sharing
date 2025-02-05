from typing import List
from app.GUI.model.models import SchedulePairingManagement
from app.BLL.Interfaces.ISchedulePairingManagementService import ISchedulePairingManagementService
from app.DAL.Interfaces.ISchedulePairingManagementRepository import ISchedulePairingManagementRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class SchedulePairingManagementService(ISchedulePairingManagementService):

    @inject
    def __init__(self, schedule_management_repository: ISchedulePairingManagementRepository, tm: TransactionManager):
        self.schedule_management_repository = schedule_management_repository
        self.tm = tm

    def get_schedule_pairing_management_of_user(self, user_id):
        with self.tm.transaction('Lỗi khi tạo schedule pairing management') as session:
            schedule_pairing_management = self.schedule_management_repository.get_schedule_pairing_management_of_user(session=session, user_id=user_id)
            if not schedule_pairing_management:
                schedule_pairing_management_raw = SchedulePairingManagement(user_id=user_id)
                schedule_pairing_management = self.schedule_management_repository\
                                            .create_schedule_pairing_management_of_user(session=session, schedule_pairing_management=schedule_pairing_management_raw)
            return schedule_pairing_management
        