from abc import ABC, abstractmethod
from app.GUI.model.models import ScheduleManagement
from typing import List
from sqlalchemy.orm import Session

class IScheduleManagementRepository(ABC):

    @abstractmethod
    def create_schedule_management(self, session: Session, schedule_management: ScheduleManagement) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_all_schedule_management(self, session: Session) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_schedule_management_by_schedule_management_id(self, session: Session, schedule_management_id: int) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_all_schedule_management_by_user_id(self, session: Session, user_id: int) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_all_schedule_managements_opening(self, session: Session) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def update_schedule_management(self, session: Session, schedule_management_id: int, data: dict) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_schedule_management_by_id(self, session: Session, schedule_management_id: int) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_some_schedule_management_by_ids(self, session: Session, list_schedule_management_id: List[int]) -> List[ScheduleManagement]:
        pass