from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import SchedulePairingManagement

class ISchedulePairingManagementService(ABC):

    @abstractmethod
    def get_schedule_pairing_management_of_user(self, user_id) -> SchedulePairingManagement:
        pass
    