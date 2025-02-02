from abc import ABC, abstractmethod
from app.GUI.model.models import ScheduleShare, RoadmapShare
from typing import List

class IScheduleShareRepository(ABC):

    @abstractmethod
    def get_schedule_share_by_id(self, schedule_share_id) -> ScheduleShare:
        pass

    @abstractmethod
    def get_schedule_share_by_departure_date(self, departure_date) -> ScheduleShare:
        pass

    @abstractmethod
    def get_schedule_share_by_departure_date_with_roadmap_open(self, departure_date) -> ScheduleShare:
        pass

    @abstractmethod
    def add_roadmaps_share_to_schedule_share(self, schedule_share: ScheduleShare, list_roadmap: List[RoadmapShare]) -> ScheduleShare:
        pass

    @abstractmethod
    def update_schedule_share(self, conditions: dict, data: dict) -> ScheduleShare:
        pass

    @abstractmethod
    def create_schedule_share(self, schedule_share) -> ScheduleShare:
        pass

    
