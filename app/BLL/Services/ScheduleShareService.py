from typing import List
from app.GUI.model.models import ScheduleShare
from app.BLL.Interfaces.IScheduleShareService import IScheduleShareService
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository

class ScheduleShareService(IScheduleShareService):

    def __init__(self, schedule_share_repository: IScheduleShareRepository):
        self.schedule_share_repository = schedule_share_repository

    def update_schedule_share(self, conditions, data):
        try:
            return self.schedule_share_repository.update_schedule_share(conditions=conditions, data=data)
        except Exception as e:
            raise e
        
    def update_schedules_share(self, conditions, data):
        try:
            return self.schedule_share_repository.update_schedules_share(conditions=conditions, data=data)
        except Exception as e:
            raise e
        
    def get_schedule_share_by_id(self, schedule_share_id):
        return self.schedule_share_repository.get_schedule_share_by_id(schedule_share_id=schedule_share_id)

    def get_schedule_share_by_departure_date(self, departure_date):
        return self.schedule_share_repository.get_schedule_share_by_departure_date(departure_date=departure_date)
    
    
    

