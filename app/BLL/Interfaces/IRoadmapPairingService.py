from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import RoadmapPairing

class IRoadmapPairingService(ABC):

    @abstractmethod
    def get_roadmap_pairing_by_id(self, roadmap_pairing_id) -> RoadmapPairing:
        pass

    @abstractmethod
    def create_roadmap_pairing(self, data: dict) -> RoadmapPairing:
        pass