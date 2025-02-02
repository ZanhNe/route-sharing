from typing import List
from app.GUI.model.models import SchedulePairingManagement
from app.BLL.Interfaces.ISchedulePairingManagementService import ISchedulePairingManagementService
from app.DAL.Interfaces.ISchedulePairingManagementRepository import ISchedulePairingManagementRepository

class SchedulePairingManagementService(ISchedulePairingManagementService):

    def __init__(self, schedule_management_repository: ISchedulePairingManagementRepository):
        self.schedule_management_repository = schedule_management_repository

    def get_schedule_pairing_management_of_user(self, user_id):
        try:
            schedule_pairing_management = self.schedule_management_repository.get_schedule_pairing_management_of_user(user_id=user_id)
            if not schedule_pairing_management:
                schedule_pairing_management_raw = SchedulePairingManagement(user_id=user_id)
                schedule_pairing_management = self.schedule_management_repository\
                                            .create_schedule_pairing_management_of_user(schedule_pairing_management=schedule_pairing_management_raw)
            return schedule_pairing_management
        except Exception as e:
            print(e)
            raise e