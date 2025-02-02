from abc import ABC, abstractmethod
from app.GUI.model.models import SchedulePairingManagement
from typing import List

class ISchedulePairingManagementRepository(ABC):

    @abstractmethod
    def get_schedule_pairing_management_of_user(self, user_id) -> SchedulePairingManagement:
        pass

    @abstractmethod
    def create_schedule_pairing_management_of_user(self, schedule_pairing_management: SchedulePairingManagement) -> SchedulePairingManagement:
        pass
