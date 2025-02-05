from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from typing import List
from app.GUI.model.models import RoadmapPairing
from sqlalchemy.exc import SQLAlchemyError
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class RoadmapPairingService(IRoadmapPairingService):
    @inject
    def __init__(self, roadmap_pairing_repository: IRoadmapPairingRepository, tm: TransactionManager):
        self.roadmap_pairing_repository = roadmap_pairing_repository
        self.tm = tm

    def get_roadmap_pairing_by_id(self, roadmap_pairing_id):
        with self.tm.transaction('') as session: 
            return self.roadmap_pairing_repository.get_roadmap_pairing_by_id(session=session, roadmap_pairing_id=roadmap_pairing_id)
    
    def create_roadmap_pairing(self, data: dict):
        with self.tm.transaction('Lỗi khi tạo roadmap pairing') as session:
            roadmap_pairing_raw = RoadmapPairing(roadmap_request_id=data['roadmap_request_id'])
            roadmap_pairing_create = self.roadmap_pairing_repository.create_roadmap_pairing(session=session, roadmap_pairing=roadmap_pairing_raw)
            return roadmap_pairing_create
        