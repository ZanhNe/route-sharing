from typing import List
from app.GUI.model.models import RoadmapShare
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RoadmapShareRepository(IRoadmapShareRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_roadmaps_share_by_schedule_share_id(self, schedule_share_id):
        return self.session.query(RoadmapShare).filter(RoadmapShare.schedule_share_id == schedule_share_id).all()
    
    def get_roadmap_share_by_id(self, roadmap_share_id):
        return self.session.query(RoadmapShare).get(ident=roadmap_share_id)
    
    def create_roadmap_share(self, roadmap_share):
        pass