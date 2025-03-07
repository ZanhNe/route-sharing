from typing import List
from app.GUI.model.models import RoadmapPairing, SchedulePairing, SchedulePairingManagement, StatusMatch
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapPairingRepository(IRoadmapPairingRepository):

    def get_roadmap_pairing_by_id(self, session: Session, roadmap_pairing_id):
        return session.query(RoadmapPairing).get(ident=roadmap_pairing_id)
    
    def get_roadmaps_pairing_by_schedule_pairing_id(self, session: Session, schedule_pairing_id) -> List[RoadmapPairing]:
        schedule_pairing = session.query(SchedulePairing).filter(SchedulePairing.id == schedule_pairing_id).first()
        roadmaps_pairing = schedule_pairing.list_roadmap_pairings.all()
        return roadmaps_pairing

    def get_in_progress_roadmap_pairings(self, session: Session, user_id) -> RoadmapPairing:
        query = session.query(RoadmapPairing)\
            .join(RoadmapPairing.list_schedule_pairings)\
            .join(SchedulePairing.schedule_pairing_management)\
            .filter(
                SchedulePairingManagement.user_id == user_id,
                RoadmapPairing.status == StatusMatch.IN_PROGRESS
            )
        return query.first()
    
    def get_roadmaps_pairing_by_ids(self, session, roadmap_pairing_ids):
        query = session.query(RoadmapPairing).filter(RoadmapPairing.id.in_(roadmap_pairing_ids))
        return query.all()

    def get_roadmaps_pairing_by_departure_date_and_user_id(self, session, user_id, departure_date):
        query = session.query(RoadmapPairing)\
                        .join(RoadmapPairing.list_schedule_pairings)\
                        .join(SchedulePairing.schedule_pairing_management)\
                        .filter(SchedulePairingManagement.user_id == user_id, SchedulePairing.departure_date == departure_date)
        return query.all()


    def create_roadmap_pairing(self, session: Session, roadmap_pairing):
        session.add(roadmap_pairing)
        return roadmap_pairing

    def update_roadmap_pairing(self, session, roadmap_pairing_id, data_update):
        query = session.query(RoadmapPairing)
        query.filter(RoadmapPairing.id == roadmap_pairing_id).update(values=data_update)
        session.flush()
        return query.get(ident=roadmap_pairing_id)
    
    def update_roadmaps_pairing(self, session, roadmap_pairing_ids, data_update):
        query = session.query(RoadmapPairing)
        query.filter(RoadmapPairing.id.in_(roadmap_pairing_ids)).update(values=data_update)
        session.flush()
        return query.filter(RoadmapPairing.id.in_(roadmap_pairing_ids)).all()
        