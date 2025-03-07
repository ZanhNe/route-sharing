from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService
from app.DAL.Interfaces.IRoadmapPairingRepository import IRoadmapPairingRepository
from typing import List
from app.GUI.model.models import RoadmapPairing, StatusMatch
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
    
    def get_roadmaps_pairing_by_schedule_pairing_id(self, schedule_pairing_id, user_id):
        with self.tm.transaction('') as session:
            roadmaps_pairing = self.roadmap_pairing_repository.get_roadmaps_pairing_by_schedule_pairing_id(session=session, schedule_pairing_id=schedule_pairing_id)
            return roadmaps_pairing
        
    def get_roadmaps_pairing_by_departure_date_and_user_id(self, user_id, departure_date):
        with self.tm.transaction('') as session:
            return self.roadmap_pairing_repository\
                    .get_roadmaps_pairing_by_departure_date_and_user_id(session=session, user_id=user_id, departure_date=departure_date)
    
    def check_outdate_roadmap_pairing(self, roadmap_pairing_id):
        with self.tm.transaction('') as session:
            roadmap_pairing = self.roadmap_pairing_repository.get_roadmap_pairing_by_id(session=session, roadmap_pairing_id=roadmap_pairing_id)
            if not roadmap_pairing:
                raise Exception('Khong tim thay Roadmap Pairing')
            if roadmap_pairing.status == StatusMatch.NOT_STARTED:
                roadmap_pairing = self.roadmap_pairing_repository\
                    .update_roadmap_pairing(session=session, roadmap_pairing_id=roadmap_pairing_id, data_update={'status': StatusMatch.CANCELLED})
                return roadmap_pairing
            
            return None
            


    def get_roadmaps_pairing_by_ids(self, roadmap_pairing_ids) -> List[RoadmapPairing]:
        with self.tm.transaction('') as session:
            roadmaps_pairing = self.roadmap_pairing_repository.get_roadmaps_pairing_by_ids(session=session, roadmap_pairing_ids=roadmap_pairing_ids)
            return roadmaps_pairing

    def get_in_progress_roadmap_pairings(self, user_id) -> RoadmapPairing:
        with self.tm.transaction('') as session:
            roadmap_pairing = self.roadmap_pairing_repository.get_in_progress_roadmap_pairings(session=session, user_id=user_id)
            return roadmap_pairing

    def create_roadmap_pairing(self, data: dict):
        with self.tm.transaction('Lỗi khi tạo roadmap pairing') as session:
            roadmap_pairing_raw = RoadmapPairing(roadmap_request_id=data['roadmap_request_id'])
            roadmap_pairing_create = self.roadmap_pairing_repository.create_roadmap_pairing(session=session, roadmap_pairing=roadmap_pairing_raw)
            return roadmap_pairing_create
        


    def update_roadmap_pairing(self, user_id, roadmap_pairing_id, data_update: dict) -> RoadmapPairing:
        with self.tm.transaction('Lỗi khi cập nhật Roadmap Pairing') as session:
            roadmap_pairing = self.get_roadmap_pairing_by_id(roadmap_pairing_id=roadmap_pairing_id)
            if not roadmap_pairing:
                raise Exception('Không tìm thấy Roadmap Pair')
            if roadmap_pairing.roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != user_id:
                raise Exception('Không có quyền sửa đổi tài nguyên của người khác')
            roadmap_pairing = self.roadmap_pairing_repository\
                .update_roadmap_pairing(session=session, roadmap_pairing_id=roadmap_pairing_id, data_update=data_update)
            return roadmap_pairing      
              
    def update_roadmaps_pairing(self, user_id, roadmap_pairing_ids, data_update):
        with self.tm.transaction('Lỗi khi cập nhật Roadmaps Pairing') as session:
            roadmaps_pairing = self.\
                get_roadmaps_pairing_by_ids(roadmap_pairing_ids=roadmap_pairing_ids)
            for rp in roadmaps_pairing:
                if rp.roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != user_id:
                    raise Exception('Không có quyền sửa đổi tài nguyên của người khác')

            roadmaps_pairing = self.roadmap_pairing_repository\
                .update_roadmaps_pairing(session=session, roadmap_pairing_ids=roadmap_pairing_ids, data_update=data_update) 
            return roadmaps_pairing
        
    def update_roadmaps_pairing_secondary_user(self, roadmap_pairing_ids, data_update):
        with self.tm.transaction('Lỗi khi cập nhật Roadmaps Pairing') as session:
            roadmaps_pairing = self.roadmap_pairing_repository\
                            .update_roadmaps_pairing(session=session, roadmap_pairing_ids=roadmap_pairing_ids, data_update=data_update)
            return roadmaps_pairing