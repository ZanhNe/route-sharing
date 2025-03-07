from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.DAL.Interfaces.IRoadmapRequestRepository import IRoadmapRequestRepository
from typing import List
from app.GUI.model.models import RoadmapRequest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class RoadmapRequestService(IRoadmapRequestService):
    @inject
    def __init__(self, roadmap_request_repository: IRoadmapRequestRepository, tm: TransactionManager):
        self.roadmap_request_repository = roadmap_request_repository
        self.tm = tm

    def get_roadmap_request_by_request_id(self, roadmap_request_id):
        with self.tm.transaction('') as session:    
            return self.roadmap_request_repository.get_roadmap_request_by_request_id(session=session, roadmap_request_id=roadmap_request_id)
    
    def get_roadmaps_request_by_roadmap_share_id(self, roadmap_share_id):
        with self.tm.transaction('') as session:    
            return self.roadmap_request_repository.get_roadmaps_request_by_roadmap_share_id(session=session, roadmap_share_id=roadmap_share_id)
    
    def get_roadmaps_request_by_sender_id(self, sender_id):
        with self.tm.transaction('') as session:
            return self.roadmap_request_repository.get_roadmaps_request_by_sender_id(session=session, sender_id=sender_id)

    def get_roadmap_request_by_roadmap_share_id_and_sender_id(self, roadmap_share_id, sender_id):
        with self.tm.transaction('') as session:
            return self.roadmap_request_repository.get_roadmap_request_by_roadmap_share_id_and_sender_id(session=session, roadmap_share_id=roadmap_share_id, sender_id=sender_id)

    def update_accept_status_roadmap_request(self, sender_id: int, roadmap_request_id, roadmap_share_id):
        with self.tm.transaction('Lỗi khi update trạng thái accept cho roadmap request') as session:
            return self.roadmap_request_repository.update_accept_status_roadmap_request(session=session, sender_id=sender_id, roadmap_request_id=roadmap_request_id, roadmap_share_id=roadmap_share_id)

    def update_declined_status_roadmap_request(self, sender_id, roadmap_request_id) -> RoadmapRequest:
        with self.tm.transaction('Lỗi khi update trạng thái decline cho roadmap request') as session:
            return self.roadmap_request_repository.update_declined_status_roadmap_request(session=session, sender_id=sender_id, roadmap_request_id=roadmap_request_id)
    
    def update_cancel_status_roadmap_request(self, session: Session, roadmap_request_id) -> RoadmapRequest:
        with self.tm.transaction('Lỗi khi updae trạng thái của roadmap request') as session:
            return self.roadmap_request_repository.update_cancel_status_roadmap_request(session=session, roadmap_request_id=roadmap_request_id)


    def add_new_roadmap_request(self, validator: dict, route_id: int, roadmap_share_id: int):
        with self.tm.transaction('Lỗi khi thêm roadmap request') as session:
            roadmap_request = RoadmapRequest(roadmap_share_id=roadmap_share_id, route_id=route_id, sender_id=validator['sender_id'])
            return self.roadmap_request_repository.create_roadmap_request(session=session, roadmap_request=roadmap_request)
        
        