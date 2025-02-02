from typing import List
from app.GUI.model.models import RoadmapPairing
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapPairingRepository(IRoadmapPairingRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_roadmap_pairing_by_id(self, roadmap_pairing_id):
        return self.session.query(RoadmapPairing).get(ident=roadmap_pairing_id)
    
    def create_roadmap_pairing(self, roadmap_pairing):
        try:
            self.session.add(roadmap_pairing)
            self.session.commit()
            return roadmap_pairing
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise Exception('Lỗi khi tạo lộ trình ghép cặp')
        