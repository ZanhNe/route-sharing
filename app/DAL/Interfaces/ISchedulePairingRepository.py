from abc import ABC, abstractmethod
from app.GUI.model.models import SchedulePairing
from typing import List
from sqlalchemy.orm import Session

class ISchedulePairingRepository(ABC):

    @abstractmethod
    def get_schedule_pairing_by_schedule_pairing_management_id(self, session: Session, schedule_pairing_management_id: int) -> SchedulePairing:
        pass

    @abstractmethod
    def get_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(self, session: Session, departure_date, schedule_pairing_management_id) -> SchedulePairing:
        pass

    @abstractmethod
    def create_schedule_pairing(self, session: Session, schedule_pairing: SchedulePairing) -> SchedulePairing:
        pass

    @abstractmethod
    def update_schedule_pairing(self, session: Session, schedule_pairing: SchedulePairing) -> SchedulePairing:
        pass

