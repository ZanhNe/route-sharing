from typing import List
from app.GUI.model.models import RoadmapShare
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapShareRepository(IRoadmapShareRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_roadmaps_share_by_schedule_share_id(self, schedule_share_id):
        return self.session.query(RoadmapShare).filter(RoadmapShare.schedule_share_id == schedule_share_id).all()
    
    def get_roadmap_share_by_schedule_share_id(self, schedule_share_id):
        return self.session.query(RoadmapShare).filter(RoadmapShare.schedule_share_id == schedule_share_id).order_by(RoadmapShare.estimated_departure_time.asc()).first()
    

    def get_roadmap_share_by_id(self, roadmap_share_id):
        return self.session.query(RoadmapShare).get(ident=roadmap_share_id)
    
    def create_roadmap_share(self, roadmap_share):
        pass

    # def update_datetime_roadmap_share_by_schedule_share_id(self, schedule_share_id: int, date_update: str) -> bool:
    #     try:
    #         query = text(
    #         """
    #         update roadmap_share 
    #         set estimated_departure_time = concat(:date_update, ' ', time(estimated_departure_time))
    #         set estimated_arrival_time = concat(:date_update, ' ', time(estimated_arrival_time))
    #         where schedule_share_id = :schedule_share_id
    #         """
    #     )
    #         self.session.execute(query, {'date_update': date_update, 'schedule_share_id': schedule_share_id})
    #         self.session.commit()
    #         return True
    #     except SQLAlchemyError as e:
    #         print(e)
    #         self.session.rollback()
    #         raise Exception('')
