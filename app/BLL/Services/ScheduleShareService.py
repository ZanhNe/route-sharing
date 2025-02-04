from typing import List
from app.GUI.model.models import ScheduleShare
from app.BLL.Interfaces.IScheduleShareService import IScheduleShareService
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class ScheduleShareService(IScheduleShareService):

    def __init__(self, schedule_share_repository: IScheduleShareRepository):
        self.schedule_share_repository = schedule_share_repository

    def update_schedule_share(self, session: Session, conditions, data):
        try:
            schedule_share = self.schedule_share_repository.update_schedule_share(session=session, conditions=conditions, data=data)
            session.commit()
            return schedule_share
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise Exception('Lỗi khi update schedule share')
        finally:
            session.close()
        
    def update_schedules_share(self, session: Session, conditions, data):
        try:
            schedules_share = self.schedule_share_repository.update_schedules_share(session=session, conditions=conditions, data=data)
            session.commit()
            return schedules_share
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise Exception('Lỗi khi update schedules share')
        finally:
            session.close()
        
    def get_schedule_share_by_id(self, session: Session, schedule_share_id):
        return self.schedule_share_repository.get_schedule_share_by_id(session=session, schedule_share_id=schedule_share_id)

    def get_schedule_share_by_departure_date(self, session: Session, departure_date):
        return self.schedule_share_repository.get_schedule_share_by_departure_date(session=session, departure_date=departure_date)
    
    
    

