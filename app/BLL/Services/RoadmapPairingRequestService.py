from app.BLL.Interfaces.IRoadmapPairingRequestService import IRoadmapPairingRequestService
from app.DAL.Interfaces.IRoadmapPairingRequestRepository import IRoadmapPairingRequestRepository
from typing import List
from app.GUI.model.models import RoadmapPairingRequest
from sqlalchemy.exc import SQLAlchemyError
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class RoadmapPairingRequestService(IRoadmapPairingRequestService):

    @inject
    def __init__(self, roadmap_pairing_request_repo: IRoadmapPairingRequestRepository, tm: TransactionManager):
        self.roadmap_pairing_request_repo = roadmap_pairing_request_repo
        self.tm = tm

    def get_roadmaps_pairing_request_by_user_id(self, user_id):
        with self.tm.transaction('') as session:
            return self.roadmap_pairing_request_repo.get_roadmaps_pairing_request_by_user_id(session=session, user_id=user_id)

    def get_roadmaps_pairing_request_by_secondary_user(self, secondary_user_id):
        with self.tm.transaction('') as session:
            return self.roadmap_pairing_request_repo.get_roadmaps_pairing_request_by_secondary_user(session=session, secondary_user_id=secondary_user_id)


    def update_roadmaps_pairing_request_by_user_id(self, user_id, data_update):
        with self.tm.transaction('') as session:
            self.roadmap_pairing_request_repo.update_roadmaps_pairing_request_by_user_id(session=session, user_id=user_id, data_update=data_update)
        
    def update_roadmaps_pairing_request_secondary_user(self, secondary_user_id, data_update):
        with self.tm.transaction('') as session:
            self.roadmap_pairing_request_repo\
                .update_roadmaps_pairing_request_secondary_user(session=session, secondary_user_id=secondary_user_id, data_update=data_update)
    
    def update_roadmap_pairing_request(self, roadmap_pairing_request_id, data_update):
        with self.tm.transaction('') as session:
            self.roadmap_pairing_request_repo.update_roadmap_pairing_request(session=session, roadmap_pairing_request_id=roadmap_pairing_request_id, data_update=data_update)
        
    def get_roadmap_pairing_request_by_id(self, roadmap_pairing_request_id: int) -> RoadmapPairingRequest:
        with self.tm.transaction('') as session:
            return self.roadmap_pairing_request_repo.get_roadmap_pairing_request_by_id(session=session, roadmap_pairing_request_id=roadmap_pairing_request_id)
        
    def save_roadmap_pairing_request(self, roadmap_pairing_request: RoadmapPairingRequest) -> RoadmapPairingRequest:
        with self.tm.transaction('') as session:
            self.roadmap_pairing_request_repo.save_roadmap_pairing_request(session=session, roadmap_pairing_request=roadmap_pairing_request)
