from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import SchedulePairing

class ISchedulePairingService(ABC):

    @abstractmethod
    def get_or_create_schedule_pairing_by_schedule_pairing_management_id(self, schedule_pairing_management_id: int) -> SchedulePairing:
        pass


    @abstractmethod
    def get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(self, departure_date, schedule_pairing_management_id: int) -> SchedulePairing:
        pass

    @abstractmethod
    def update_schedule_pairing(self, schedule_pairing: SchedulePairing) -> SchedulePairing:
        pass