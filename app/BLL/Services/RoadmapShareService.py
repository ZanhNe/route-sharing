from app.BLL.Interfaces.IRoadmapShareService import IRoadmapShareService
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from typing import List
from app.GUI.model.models import RoadmapShare

class RoadmapShareService(IRoadmapShareService):

    def __init__(self, roadmap_share_repo: IRoadmapShareRepository):
        self.roadmap_share_repo = roadmap_share_repo

    def get_roadmaps_share_by_schedule_share_id(self, schedule_share_id):
        return self.roadmap_share_repo.get_roadmaps_share_by_schedule_share_id(schedule_share_id=schedule_share_id)
    
    def get_roadmap_share_by_schedule_share_id(self, schedule_share_id):
        return self.roadmap_share_repo.get_roadmap_share_by_schedule_share_id(schedule_share_id=schedule_share_id)


    def get_roadmap_share_by_id(self, roadmap_share_id):
        return self.roadmap_share_repo.get_roadmap_share_by_id(roadmap_share_id=roadmap_share_id)
    
    def create_roadmap_share(self, roadmap_share):
        pass