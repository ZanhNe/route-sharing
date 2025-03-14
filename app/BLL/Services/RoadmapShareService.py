from app.BLL.Interfaces.IRoadmapShareService import IRoadmapShareService
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from typing import List
from app.GUI.model.models import RoadmapShare
from sqlalchemy.orm import Session
from app.custom.Helper.Helper import TransactionManager
from injector import inject
from datetime import datetime


class RoadmapShareService(IRoadmapShareService):
    @inject
    def __init__(self, roadmap_share_repo: IRoadmapShareRepository, tm: TransactionManager):
        self.roadmap_share_repo = roadmap_share_repo
        self.tm = tm

    def get_roadmaps_share_by_schedule_share_id(self, schedule_share_id):
        with self.tm.transaction('') as session:
            return self.roadmap_share_repo.get_roadmaps_share_by_schedule_share_id(session=session, schedule_share_id=schedule_share_id)
    
    def get_roadmap_share_by_schedule_share_id(self, schedule_share_id):
        with self.tm.transaction('') as session:
            return self.roadmap_share_repo.get_roadmap_share_by_schedule_share_id(session=session, schedule_share_id=schedule_share_id)


    def get_roadmaps_share_by_schedule_share_id_is_open(self, schedule_share_id):
        with self.tm.transaction('') as session:
            return self.roadmap_share_repo.get_roadmaps_share_by_schedule_share_id_is_open(session=session, schedule_share_id=schedule_share_id)

    def get_roadmap_share_by_id(self, roadmap_share_id):
        with self.tm.transaction('') as session:
            return self.roadmap_share_repo.get_roadmap_share_by_id(session=session, roadmap_share_id=roadmap_share_id)
    
    def create_roadmap_share(self, roadmap_share):
        pass

    def update_roadmap_share(self, roadmap_share_id, data_update):
        with self.tm.transaction('Lỗi khi update Roadmap share') as session:
            return self.roadmap_share_repo.update_roadmap_share(session=session, roadmap_share_id=roadmap_share_id, data_update=data_update)
        
    def check_outdate_roadmaps_share(self):
        with self.tm.transaction('Lỗi khi update Roadmaps share') as session:
            self.roadmap_share_repo.update_roadmaps_share_by_schedule_share_id(session=session, data_update={'is_open': False, 'time': datetime.now()})
    