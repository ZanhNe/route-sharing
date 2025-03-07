from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import ScheduleManagement, ScheduleShare, Route, RoadmapPairing
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

    @abstractmethod
    def handle_declined_roadmap_request(self, roadmap_request_id: int, main_user_id: str):
        pass
    
    @abstractmethod
    def handle_update_roadmap_pairing(self, roadmap_pairing_id: int, user_id, data_update: dict):
        pass

    @abstractmethod
    def handle_start_roadmap_pairing(self, user_id, roadmap_pairing_id: int):
        pass

    @abstractmethod
    def handle_end_roadmap_pairing(self, user_id, roadmap_pairing_id: int) -> RoadmapPairing:
        pass

    @abstractmethod
    def check_outdate_schedule_share(self):
        pass

    @abstractmethod
    def send_roadmap_pairing_request(self, sender_id, roadmap_pairing_id: int):
        pass

    @abstractmethod
    def accept_roadmap_pairing_request(self, secondary_user_id, roadmap_pairing_id, roadmap_pairing_request_id):
        pass

    @abstractmethod
    def decline_roadmap_pairing_request(self, secondary_user_id, roadmap_pairing_request_id):
        pass