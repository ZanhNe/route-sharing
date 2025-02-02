from abc import ABC, abstractmethod
from app.GUI.model.models import ScheduleManagement
from typing import List

class IScheduleManagementRepository(ABC):

    @abstractmethod
    def create_schedule_management(self, schedule_management: ScheduleManagement) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_all_schedule_management(self) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_schedule_management_by_schedule_management_id(self, schedule_management_id: int) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_all_schedule_management_by_user_id(self, user_id: int) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_all_schedule_managements_opening(self) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def update_schedule_management(self, schedule_management_id: int, data: dict) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_schedule_management_by_id(self, schedule_management_id: int) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_some_schedule_management_by_ids(self, list_schedule_management_id: List[int]) -> List[ScheduleManagement]:
        pass