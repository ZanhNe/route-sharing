from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import ScheduleManagement, ScheduleShare, Route
from app.lib.lib_ma import ScheduleManagementSchema

class IScheduleManagementShareRoute(ABC):

    @abstractmethod
    def handle_schedule_share(self, schedule_setup_informations: dict) -> List[ScheduleShare]:
        pass
    
