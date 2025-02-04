from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.DAL.Interfaces.IRoadmapRequestRepository import IRoadmapRequestRepository
from typing import List
from app.GUI.model.models import RoadmapRequest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

class RoadmapRequestService(IRoadmapRequestService):

    def __init__(self, roadmap_request_repository: IRoadmapRequestRepository):
        self.roadmap_request_repository = roadmap_request_repository

    def get_roadmap_request_by_request_id(self, session: Session, roadmap_request_id):
        return self.roadmap_request_repository.get_roadmap_request_by_request_id(session=session, roadmap_request_id=roadmap_request_id)
    
    def get_roadmaps_request_by_roadmap_share_id(self, session: Session, roadmap_share_id):
        return self.roadmap_request_repository.get_roadmaps_request_by_roadmap_share_id(session=session, roadmap_share_id=roadmap_share_id)
    
    def get_roadmaps_request_by_sender_id(self, session: Session, sender_id):
        return self.roadmap_request_repository.get_roadmaps_request_by_sender_id(session=session, sender_id=sender_id)

    def get_roadmap_request_by_roadmap_share_id_and_sender_id(self, session: Session, roadmap_share_id, sender_id):
        return self.roadmap_request_repository.get_roadmap_request_by_roadmap_share_id_and_sender_id(session=session, roadmap_share_id=roadmap_share_id, sender_id=sender_id)

    def update_accept_status_roadmap_request(self, session: Session, sender_id: int, roadmap_request_id, roadmap_share_id):
        return self.roadmap_request_repository.update_accept_status_roadmap_request(session=session, sender_id=sender_id, roadmap_request_id=roadmap_request_id, roadmap_share_id=roadmap_share_id)

    def update_declined_status_roadmap_request(self, session: Session, sender_id, roadmap_request_id) -> RoadmapRequest:
        return self.roadmap_request_repository.update_declined_status_roadmap_request(session=session, sender_id=sender_id, roadmap_request_id=roadmap_request_id)
    

    def add_new_roadmap_request(self, session: Session, validator: dict, route_id: int, roadmap_share_id: int):
        try:
            roadmap_request = RoadmapRequest(roadmap_share_id=roadmap_share_id, route_id=route_id, sender_id=validator['sender_id'])
            return self.roadmap_request_repository.create_roadmap_request(session=session, roadmap_request=roadmap_request)
        except SQLAlchemyError as e:
            raise e
        