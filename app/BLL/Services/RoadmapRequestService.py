from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.DAL.Interfaces.IRoadmapRequestRepository import IRoadmapRequestRepository
from typing import List
from app.GUI.model.models import RoadmapRequest
from sqlalchemy.exc import SQLAlchemyError

class RoadmapRequestService(IRoadmapRequestService):

    def __init__(self, roadmap_request_repository: IRoadmapRequestRepository):
        self.roadmap_request_repository = roadmap_request_repository

    def get_roadmap_request_by_request_id(self, roadmap_request_id):
        return self.roadmap_request_repository.get_roadmap_request_by_request_id(roadmap_request_id=roadmap_request_id)
    
    def get_roadmaps_request_by_roadmap_share_id(self, roadmap_share_id):
        return self.roadmap_request_repository.get_roadmaps_request_by_roadmap_share_id(roadmap_share_id=roadmap_share_id)
    
    def get_roadmap_request_by_roadmap_share_id_and_sender_id(self, roadmap_share_id, sender_id):
        return self.roadmap_request_repository.get_roadmap_request_by_roadmap_share_id_and_sender_id(roadmap_share_id=roadmap_share_id, sender_id=sender_id)


    def add_new_roadmap_request(self, validator: dict, route_id: int, roadmap_share_id: int):
        try:
            roadmap_request = RoadmapRequest(roadmap_share_id=roadmap_share_id, route_id=route_id, sender_id=validator['sender_id'])
            return self.roadmap_request_repository.create_roadmap_request(roadmap_request=roadmap_request)
        except SQLAlchemyError as e:
            raise e
        