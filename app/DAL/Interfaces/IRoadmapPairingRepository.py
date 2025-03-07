from abc import ABC, abstractmethod
from app.GUI.model.models import RoadmapPairing
from typing import List
from sqlalchemy.orm import Session


class IRoadmapPairingRepository(ABC):

    @abstractmethod
    def get_roadmap_pairing_by_id(self, session: Session, roadmap_pairing_id) -> RoadmapPairing:
        pass

    @abstractmethod
    def get_roadmaps_pairing_by_schedule_pairing_id(self, session: Session, schedule_pairing_id) -> List[RoadmapPairing]:
        pass

    @abstractmethod
    def get_roadmaps_pairing_by_departure_date_and_user_id(self, session: Session, user_id, departure_date) -> List[RoadmapPairing]:
        pass

    @abstractmethod
    def get_roadmaps_pairing_by_ids(self, session: Session, roadmap_pairing_ids: List[int]) -> List[RoadmapPairing]:
        pass

    @abstractmethod
    def get_in_progress_roadmap_pairings(self, session: Session, user_id) -> RoadmapPairing:
        pass

    @abstractmethod
    def create_roadmap_pairing(self, session: Session, roadmap_pairing: RoadmapPairing) -> RoadmapPairing:
        pass


    @abstractmethod
    def update_roadmap_pairing(self, session: Session, roadmap_pairing_id: int, data_update: dict) -> RoadmapPairing:
        pass

    @abstractmethod
    def update_roadmaps_pairing(self, session: Session, roadmap_pairing_ids: List[int], data_update: dict) -> List[RoadmapPairing]:
        pass
    