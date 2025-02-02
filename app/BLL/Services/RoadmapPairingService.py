from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from typing import List
from app.GUI.model.models import RoadmapPairing
from sqlalchemy.exc import SQLAlchemyError

class RoadmapPairingService(IRoadmapPairingService):

    def __init__(self, roadmap_pairing_repository: IRoadmapPairingRepository):
        self.roadmap_pairing_repository = roadmap_pairing_repository

    def get_roadmap_pairing_by_id(self, roadmap_pairing_id):
        return self.roadmap_pairing_repository.get_roadmap_pairing_by_id(roadmap_pairing_id=roadmap_pairing_id)
    
    def create_roadmap_pairing(self, data: dict):
        try:
            roadmap_pairing_raw = RoadmapPairing(roadmap_request_id=data['roadmap_request_id'])
            roadmap_pairing_create = self.roadmap_pairing_repository.create_roadmap_pairing(roadmap_pairing=roadmap_pairing_raw)
            return roadmap_pairing_create
        except Exception as e:
            raise e