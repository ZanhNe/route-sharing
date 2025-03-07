from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import ScheduleShare

class IScheduleShareService(ABC):

    @abstractmethod
    def update_schedule_share(self, conditions: dict, data: dict):
        pass

    @abstractmethod
    def update_schedules_share(self, conditions: dict, data: dict):
        pass


    @abstractmethod
    def check_outdate_schedule(self):
        pass

    @abstractmethod
    def get_schedule_share_by_id(self, schedule_share_id):
        pass

    @abstractmethod
    def get_schedule_share_by_departure_date(self, departure_date) -> ScheduleShare:
        pass