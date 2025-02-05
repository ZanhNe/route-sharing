from abc import ABC, abstractmethod
from app.GUI.model.models import ScheduleShare, RoadmapShare
from typing import List
from sqlalchemy.orm import Session

class IScheduleShareRepository(ABC):

    @abstractmethod
    def get_schedule_share_by_id(self, session: Session, schedule_share_id) -> ScheduleShare:
        pass

    @abstractmethod
    def get_schedule_share_by_departure_date(self, session: Session, departure_date, schedule_management_id: int) -> ScheduleShare:
        pass

    @abstractmethod
    def get_schedule_share_by_departure_date_with_roadmap_open(self, session: Session, departure_date, schedule_management_id: int) -> ScheduleShare:
        pass

    @abstractmethod
    def add_roadmaps_share_to_schedule_share(self, session: Session, schedule_share: ScheduleShare, list_roadmap: List[RoadmapShare]) -> ScheduleShare:
        pass

    @abstractmethod
    def update_schedule_share(self, session: Session, conditions: dict, data: dict) -> ScheduleShare:
        pass

    @abstractmethod
    def update_schedules_share(self, session: Session, conditions: dict, data: dict) -> List[ScheduleShare]:
        pass

    @abstractmethod
    def create_schedule_share(self, session: Session, schedule_share) -> ScheduleShare:
        pass

    
