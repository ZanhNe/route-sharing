from typing import List
from app.GUI.model.models import RoadmapPairing, RoadmapPairingRequest, Status, SchedulePairing, SchedulePairingManagement
from app.DAL.Interfaces.IRoadmapPairingRequestRepository import IRoadmapPairingRequestRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapPairingRequestRepository(IRoadmapPairingRequestRepository):
    
    def update_roadmaps_pairing_request_by_user_id(self, session: Session, user_id, data_update):
        query = session.query(RoadmapPairingRequest).filter(RoadmapPairingRequest.sender_id == user_id, RoadmapPairingRequest.status == Status.PENDING)
        query.update(values=data_update)
    
    def update_roadmaps_pairing_request_secondary_user(self, session: Session, secondary_user_id, data_update):
        sq = session.query(RoadmapPairingRequest.id)\
                        .join(RoadmapPairingRequest.roadmap_pairing)\
                        .join(RoadmapPairing.list_schedule_pairings)\
                        .join(SchedulePairing.schedule_pairing_management)\
                        .filter(SchedulePairingManagement.user_id == secondary_user_id, RoadmapPairingRequest.status == Status.PENDING, RoadmapPairingRequest.sender_id != secondary_user_id)\
                        .subquery()
        session.query(RoadmapPairingRequest).filter(RoadmapPairingRequest.id.in_(sq)).update(values=data_update)
        

    def update_roadmap_pairing_request(self, session: Session, roadmap_pairing_request_id: int, data_update: dict):
        session.query(RoadmapPairingRequest).filter(RoadmapPairingRequest.id == roadmap_pairing_request_id).update(values=data_update)

    

    def get_roadmaps_pairing_request_by_user_id(self, session, user_id):
        return session\
                .query(RoadmapPairingRequest)\
                .filter(RoadmapPairingRequest.sender_id == user_id, RoadmapPairingRequest.status == Status.PENDING).order_by(RoadmapPairingRequest.created_date.desc()).all()
    
    def get_roadmaps_pairing_request_by_secondary_user(self, session, secondary_user_id):
        return session.query(RoadmapPairingRequest)\
                        .join(RoadmapPairingRequest.roadmap_pairing)\
                        .join(RoadmapPairing.list_schedule_pairings)\
                        .join(SchedulePairing.schedule_pairing_management)\
                        .filter(SchedulePairingManagement.user_id == secondary_user_id, RoadmapPairingRequest.status == Status.PENDING, RoadmapPairingRequest.sender_id != secondary_user_id)\
                        .all()
    
    def get_roadmap_pairing_request_by_id(self, session: Session, roadmap_pairing_request_id: int) -> RoadmapPairingRequest:
        return session.query(RoadmapPairingRequest).get(ident=roadmap_pairing_request_id)
    
    def save_roadmap_pairing_request(self, session: Session, roadmap_pairing_request: RoadmapPairingRequest) -> RoadmapPairingRequest:
        session.add(instance=roadmap_pairing_request)
        
    