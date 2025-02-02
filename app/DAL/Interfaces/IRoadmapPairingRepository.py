from abc import ABC, abstractmethod
from app.GUI.model.models import RoadmapPairing
from typing import List

class IRoadmapPairingRepository(ABC):

    @abstractmethod
    def get_roadmap_pairing_by_id(self, roadmap_pairing_id) -> RoadmapPairing:
        pass

    @abstractmethod
    def create_roadmap_pairing(self, roadmap_pairing: RoadmapPairing) -> RoadmapPairing:
        pass
    