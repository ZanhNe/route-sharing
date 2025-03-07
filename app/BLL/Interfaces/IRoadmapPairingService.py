from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import RoadmapPairing

class IRoadmapPairingService(ABC):

    @abstractmethod
    def get_roadmap_pairing_by_id(self, roadmap_pairing_id) -> RoadmapPairing:
        pass

    @abstractmethod
    def get_roadmaps_pairing_by_schedule_pairing_id(self, schedule_pairing_id, user_id) -> List[RoadmapPairing]:
        pass

    @abstractmethod
    def get_roadmaps_pairing_by_departure_date_and_user_id(self, user_id, departure_date):
        pass

    @abstractmethod
    def get_roadmaps_pairing_by_ids(self, roadmap_pairing_ids: List[int]) -> List[RoadmapPairing]:
        pass

    @abstractmethod
    def check_outdate_roadmap_pairing(self, roadmap_pairing_id: int) -> RoadmapPairing:
        pass

    @abstractmethod
    def get_in_progress_roadmap_pairings(self, user_id) -> RoadmapPairing:
        pass

    @abstractmethod
    def create_roadmap_pairing(self, data: dict) -> RoadmapPairing:
        pass

    @abstractmethod
    def update_roadmap_pairing(self, user_id, roadmap_pairing_id: int, data_update: dict) -> RoadmapPairing:
        pass

    @abstractmethod
    def update_roadmaps_pairing(self, user_id, roadmap_pairing_ids, data_update):
        pass

    @abstractmethod
    def update_roadmaps_pairing_secondary_user(self, roadmap_pairing_ids, data_update):
        pass
