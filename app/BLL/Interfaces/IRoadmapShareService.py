from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import RoadmapShare

class IRoadmapShareService(ABC):

    @abstractmethod
    def get_roadmap_share_by_id(self, roadmap_share_id) -> RoadmapShare:
        pass

    @abstractmethod
    def get_roadmaps_share_by_schedule_share_id(self, schedule_share_id) -> List[RoadmapShare]:
        pass

    @abstractmethod
    def get_roadmap_share_by_schedule_share_id(self, schedule_share_id) -> RoadmapShare:
        pass
 
    @abstractmethod
    def create_roadmap_share(self, roadmap_share) -> RoadmapShare:
        pass