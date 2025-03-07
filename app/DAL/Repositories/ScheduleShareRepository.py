from typing import List
from app.GUI.model.models import ScheduleShare, RoadmapShare
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from sqlalchemy.orm import Session, with_loader_criteria, selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import datetime

class ScheduleShareRepository(IScheduleShareRepository):

    def get_schedule_share_by_id(self, session: Session, schedule_share_id):
        return session.query(ScheduleShare).get(ident=schedule_share_id)
    
    def get_schedule_share_by_departure_date(self, session: Session, departure_date: datetime, schedule_management_id: int):
        return session.query(ScheduleShare)\
            .filter(ScheduleShare.departure_date == departure_date, ScheduleShare.schedule_management_id == schedule_management_id).first()
    
    def get_schedule_share_by_departure_date_with_roadmap_open(self, session: Session, departure_date: datetime, schedule_management_id: int):
        return session.query(ScheduleShare)\
            .options(selectinload(ScheduleShare.list_roadmaps), with_loader_criteria(RoadmapShare, RoadmapShare.is_open == True))\
            .filter(ScheduleShare.departure_date == departure_date, ScheduleShare.schedule_management_id == schedule_management_id).first()

    def update_schedules_share(self, session: Session, conditions: dict, data):
        query = session.query(ScheduleShare).filter(*[getattr(ScheduleShare, key) == value for key, value in conditions.items()])
        query.update(data)
        return query.all()

    def update_schedules_share_lt(self, session: Session, conditions: dict, data):
        query = session.query(ScheduleShare).filter(*[getattr(ScheduleShare, key) < value for key, value in conditions.items()])
        query.update(data)
        return query.all()
        

    def update_schedule_share(self, session: Session, conditions, data):
        query = session.query(ScheduleShare).filter(*[getattr(ScheduleShare, key) == value for key, value in conditions.items()])
        query.update(data)
        if 'departure_date' in data:
            queryText = text(
                """
                update roadmap_share 
                set estimated_departure_time = concat(:date_update, ' ', time(estimated_departure_time)),
                    estimated_arrival_time = concat(:date_update, ' ', time(estimated_arrival_time))
                where schedule_share_id = :schedule_share_id
                    """
            )
        session.execute(queryText, {'date_update': str(data['departure_date'])[0:10], 'schedule_share_id': conditions['id']})
        return query.first()

    def add_roadmaps_share_to_schedule_share(self, session: Session, schedule_share: ScheduleShare, list_roadmap: List[RoadmapShare]):
        schedule_share.list_roadmaps.extend(list_roadmap)
        return schedule_share

            
    def create_schedule_share(self, session: Session, schedule_share):
        session.add(schedule_share)
        return schedule_share