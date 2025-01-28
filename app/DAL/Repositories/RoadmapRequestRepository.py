from typing import List
from app.GUI.model.models import RoadmapRequest
from app.DAL.Interfaces.IRoadmapRequestRepository import IRoadmapRequestRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RoadmapRequestRepository(IRoadmapRequestRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_roadmap_request_by_request_id(self, roadmap_request_id):
        return self.session.query(RoadmapRequest).get(ident=roadmap_request_id)
    
    def get_roadmaps_request_by_roadmap_share_id(self, roadmap_share_id):
        return self.session.query(RoadmapRequest).filter(RoadmapRequest.roadmap_share_id == roadmap_share_id).order_by(RoadmapRequest.id.desc()).all()
    
    def get_roadmap_request_by_roadmap_share_id_and_sender_id(self, roadmap_share_id, sender_id) -> RoadmapRequest:
        return self.session.query(RoadmapRequest).filter(RoadmapRequest.roadmap_share_id == roadmap_share_id, RoadmapRequest.sender_id == sender_id).first()


    def create_roadmap_request(self, roadmap_request):
        try:
            self.session.add(instance=roadmap_request)
            self.session.commit()
            return roadmap_request
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise e