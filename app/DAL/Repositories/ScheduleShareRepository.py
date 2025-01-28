from typing import List
from app.GUI.model.models import ScheduleShare, RoadmapShare
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from sqlalchemy.orm import Session, with_loader_criteria, selectinload
from sqlalchemy.exc import SQLAlchemyError

class ScheduleShareRepository(IScheduleShareRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_schedule_share_by_id(self, schedule_share_id):
        return self.session.query(ScheduleShare).get(ident=schedule_share_id)
    
    def get_schedule_share_by_departure_date(self, departure_date):
        return self.session.query(ScheduleShare)\
            .filter(ScheduleShare.departure_date == departure_date).first()
    
    def get_schedule_share_by_departure_date_with_roadmap_open(self, departure_date):
        return self.session.query(ScheduleShare)\
            .options(selectinload(ScheduleShare.list_roadmaps), with_loader_criteria(RoadmapShare, RoadmapShare.is_open == True))\
            .filter(ScheduleShare.departure_date == departure_date).first()

    def add_roadmaps_share_to_schedule_share(self, schedule_share: ScheduleShare, list_roadmap: List[RoadmapShare]):
        try:
            schedule_share.list_roadmaps.extend(list_roadmap)
            self.session.commit()
            return schedule_share
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise e
            
            

    def create_schedule_share(self, schedule_share):
        try:
            self.session.add(schedule_share)
            self.session.commit()
            return schedule_share
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None