from typing import List
from app.GUI.model.models import RoadmapShare
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapShareRepository(IRoadmapShareRepository):

    def get_roadmaps_share_by_schedule_share_id(self, session: Session,schedule_share_id):
        return session.query(RoadmapShare).filter(RoadmapShare.schedule_share_id == schedule_share_id).order_by(RoadmapShare.estimated_departure_time.desc()).all()
    
    def get_roadmap_share_by_schedule_share_id(self, session: Session,schedule_share_id):
        return session.query(RoadmapShare).filter(RoadmapShare.schedule_share_id == schedule_share_id).order_by(RoadmapShare.estimated_departure_time.asc()).first()
    
    def get_roadmaps_share_by_schedule_share_id_is_open(self, session: Session,schedule_share_id):
        return session.query(RoadmapShare).filter(RoadmapShare.schedule_share_id == schedule_share_id, RoadmapShare.is_open == True).order_by(RoadmapShare.estimated_departure_time.desc()).all()

    def get_roadmap_share_by_id(self, session: Session,roadmap_share_id):
        return session.query(RoadmapShare).get(ident=roadmap_share_id)
    
    def create_roadmap_share(self, session: Session,roadmap_share):
        pass

    # def update_datetime_roadmap_share_by_schedule_share_id(self, session: Session,schedule_share_id: int, date_update: str) -> bool:
    #     try:
    #         query = text(
    #         """
    #         update roadmap_share 
    #         set estimated_departure_time = concat(:date_update, ' ', time(estimated_departure_time))
    #         set estimated_arrival_time = concat(:date_update, ' ', time(estimated_arrival_time))
    #         where schedule_share_id = :schedule_share_id
    #         """
    #     )
    #         session.execute(query, {'date_update': date_update, 'schedule_share_id': schedule_share_id})
    #         session.commit()
    #         return True
    #     except SQLAlchemyError as e:
    #         print(e)
    #         session.rollback()
    #         raise Exception('')
