from typing import List
from app.GUI.model.models import ScheduleShare
from app.BLL.Interfaces.IScheduleShareService import IScheduleShareService
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.custom.Helper.Helper import TransactionManager
from datetime import datetime
from injector import inject


class ScheduleShareService(IScheduleShareService):

    @inject
    def __init__(self, schedule_share_repository: IScheduleShareRepository, tm: TransactionManager):
        self.schedule_share_repository = schedule_share_repository
        self.tm = tm

    def update_schedule_share(self, conditions, data):
        with self.tm.transaction('Lỗi khi cập nhật schedule share') as session:
            schedule_share = self.schedule_share_repository.update_schedule_share(session=session, conditions=conditions, data=data)
            return schedule_share
        
        
    def update_schedules_share(self, conditions, data):
        with self.tm.transaction('Lỗi khi cập nhật schedules share') as session:
            schedules_share = self.schedule_share_repository.update_schedules_share(session=session, conditions=conditions, data=data)
            return schedules_share
        
        
    def get_schedule_share_by_id(self, schedule_share_id):
        with self.tm.transaction('') as session:
            return self.schedule_share_repository.get_schedule_share_by_id(session=session, schedule_share_id=schedule_share_id)

    def get_schedule_share_by_departure_date(self, departure_date):
        with self.tm.transaction('') as session:
            return self.schedule_share_repository.get_schedule_share_by_departure_date(session=session, departure_date=departure_date)
    
    def check_outdate_schedule(self):
        with self.tm.transaction('Lỗi khi kiểm tra outdate các lịch trình') as session:
            now = datetime.now()
            schedules_share = self.schedule_share_repository.\
                update_schedules_share_lt(session=session, conditions={'departure_date': now}, data={'is_open': False})
            

    
    

