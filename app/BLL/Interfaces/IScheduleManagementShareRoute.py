from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import ScheduleManagement, ScheduleShare, Route
from app.lib.lib_ma import ScheduleManagementSchema

class IScheduleManagementShareRoute(ABC):

    @abstractmethod
    def handle_schedule_share(self, schedule_setup_informations: dict) -> List[ScheduleShare]:
        pass

    @abstractmethod
    def add_new_request_roadmap(self, validator: dict, roadmap_share_id: int):
        pass

    @abstractmethod
    def handle_update_schedule_share(self, update_schedule_share_validator: dict):
        pass

    @abstractmethod
    def handle_accept_roadmap_request(self, roadmap_request_id: int, main_user_id: str):
        pass
    
