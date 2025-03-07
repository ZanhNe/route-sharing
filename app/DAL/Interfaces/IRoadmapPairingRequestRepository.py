from abc import ABC, abstractmethod
from app.GUI.model.models import RoadmapPairingRequest
from typing import List
from sqlalchemy.orm import Session


class IRoadmapPairingRequestRepository(ABC):

    @abstractmethod
    def update_roadmaps_pairing_request_by_user_id(self, session: Session, user_id, data_update: dict):
        pass

    @abstractmethod
    def update_roadmaps_pairing_request_secondary_user(self, session: Session, secondary_user_id, data_update):
        pass

    @abstractmethod
    def update_roadmap_pairing_request(self, session: Session, roadmap_pairing_request_id: int, data_update: dict):
        pass

    @abstractmethod
    def get_roadmaps_pairing_request_by_secondary_user(self, session: Session, secondary_user_id):
        pass

    @abstractmethod
    def get_roadmaps_pairing_request_by_user_id(self, session: Session, user_id) -> List[RoadmapPairingRequest]:
        pass

    @abstractmethod
    def get_roadmap_pairing_request_by_id(self, session: Session, roadmap_pairing_request_id: int) -> RoadmapPairingRequest:
        pass

    @abstractmethod
    def save_roadmap_pairing_request(self, session: Session, roadmap_pairing_request: RoadmapPairingRequest) -> RoadmapPairingRequest:
        pass


