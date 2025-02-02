from abc import ABC, abstractmethod
from app.GUI.model.models import RoadmapRequest
from typing import List

class IRoadmapRequestRepository(ABC):

    @abstractmethod
    def get_roadmap_request_by_request_id(self, roadmap_request_id) -> RoadmapRequest:
        pass

    @abstractmethod
    def get_roadmaps_request_by_roadmap_share_id(self, roadmap_share_id) -> List[RoadmapRequest]:
        pass

    @abstractmethod
    def get_roadmaps_request_by_sender_id(self, sender_id) -> List[RoadmapRequest]:
        pass

    @abstractmethod
    def get_roadmap_request_by_roadmap_share_id_and_sender_id(self, roadmap_share_id, sender_id) -> RoadmapRequest:
        pass

    @abstractmethod
    def update_accept_status_roadmap_request(self, sender_id: str, roadmap_request_id: int, roadmap_share_id: int) -> RoadmapRequest:
        pass

    @abstractmethod
    def create_roadmap_request(self, roadmap_request: RoadmapRequest) -> RoadmapRequest:
        pass

    