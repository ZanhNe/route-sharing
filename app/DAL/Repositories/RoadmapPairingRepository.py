from typing import List
from app.GUI.model.models import RoadmapPairing
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapPairingRepository(IRoadmapPairingRepository):

    def get_roadmap_pairing_by_id(self, session: Session, roadmap_pairing_id):
        return session.query(RoadmapPairing).get(ident=roadmap_pairing_id)
    
    def create_roadmap_pairing(self, session: Session, roadmap_pairing):
        session.add(roadmap_pairing)
        return roadmap_pairing

        