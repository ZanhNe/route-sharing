from typing import List
from app.GUI.model.models import ScheduleShare, RoadmapShare
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from sqlalchemy.orm import Session, with_loader_criteria, selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

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

    def update_schedules_share(self, conditions: dict, data):
        try:
            query = self.session.query(ScheduleShare).filter(*[getattr(ScheduleShare, key) == value for key, value in conditions.items()])
            query.update(data)
            self.session.commit()
            return query.all()
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise Exception('Lỗi khi cập nhật các lịch trình chia sẻ')
        

    def update_schedule_share(self, conditions, data):
        try:
            query = self.session.query(ScheduleShare).filter(*[getattr(ScheduleShare, key) == value for key, value in conditions.items()])
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
                self.session.execute(queryText, {'date_update': str(data['departure_date'])[0:10], 'schedule_share_id': conditions['id']})
            self.session.commit()
            return query.first()
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            raise Exception('Lỗi khi cập nhật lịch trình chia sẻ')

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