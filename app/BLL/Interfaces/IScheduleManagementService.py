from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import ScheduleManagement, Route, ScheduleShare
from app.lib.lib_ma import ScheduleManagementSchema
class IScheduleManagementService(ABC):

    @abstractmethod
    def create_schedule_management(self, schedule_management: ScheduleManagement) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_all_schedule_management(self) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_schedule_management_by_title_and_user_id(self, schedule_management_title: str, user_id: str) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_schedule_management_by_schedule_management_id(self, schedule_management_id: int) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_all_schedule_management_by_user_id(self, user_id: int) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def update_schedule_management(self, user_id, schedule_management_id: int, data: dict):
        pass
    
    @abstractmethod
    def get_all_schedule_managements_opening(self) -> List[ScheduleManagement]:
        pass

    @abstractmethod
    def get_schedule_management_by_id(self, schedule_management_id: int) -> ScheduleManagement:
        pass

    @abstractmethod
    def get_some_schedule_management_by_ids(self, list_schedule_management_id: List[int]) -> List[ScheduleManagement]:
        pass
    
    @abstractmethod
    def handle_roadmaps_share(self, schedule_management_id: int, schedule_setup_informations: dict, route: Route) -> List[ScheduleShare]:
        pass