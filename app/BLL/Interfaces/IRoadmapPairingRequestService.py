from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import RoadmapPairingRequest

class IRoadmapPairingRequestService(ABC):

    @abstractmethod
    def update_roadmaps_pairing_request_by_user_id(self, user_id, data_update: dict):
        pass

    @abstractmethod
    def update_roadmaps_pairing_request_secondary_user(self, secondary_user_id, data_update):
        pass

    @abstractmethod
    def update_roadmap_pairing_request(self, roadmap_pairing_request_id: int, data_update: dict):
        pass

    @abstractmethod
    def get_roadmaps_pairing_request_by_secondary_user(self, secondary_user_id) -> List[RoadmapPairingRequest]:
        pass

    @abstractmethod
    def get_roadmaps_pairing_request_by_user_id(self, user_id) -> List[RoadmapPairingRequest]:
        pass

    @abstractmethod
    def get_roadmap_pairing_request_by_id(self, roadmap_pairing_request_id: int) -> RoadmapPairingRequest:
        pass

    @abstractmethod
    def save_roadmap_pairing_request(self, roadmap_pairing_request: RoadmapPairingRequest) -> RoadmapPairingRequest:
        pass