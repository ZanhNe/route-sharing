from typing import List
from app.GUI.model.models import ScheduleManagement
from app.DAL.Interfaces.IScheduleManagementRepository import IScheduleManagementRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class ScheduleManagementRepository(IScheduleManagementRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_schedule_management_by_id(self, schedule_management_id: int) -> ScheduleManagement:
        return self.session.query(ScheduleManagement).get(ident=schedule_management_id)
    
    def get_schedule_management_by_schedule_management_id(self, schedule_management_id: int) -> ScheduleManagement:
        return self.session.query(ScheduleManagement)\
                    .filter(ScheduleManagement.id == schedule_management_id)\
                    .first()
    
    def get_all_schedule_management(self):
        return self.session.query(ScheduleManagement).order_by(ScheduleManagement.created_date.desc()).all()
    
    def get_all_schedule_management_by_user_id(self, user_id: int) -> List[ScheduleManagement]:
        return self.session.query(ScheduleManagement).filter(ScheduleManagement.user_id == user_id).order_by(ScheduleManagement.created_date.desc()).all()

    def get_some_schedule_management_by_ids(self, list_schedule_management_id):
        return self.session.query(ScheduleManagement).filter(ScheduleManagement.id.in_(list_schedule_management_id)).all()

    def get_all_schedule_managements_opening(self) -> List[ScheduleManagement]:
        return self.session.query(ScheduleManagement).filter(ScheduleManagement.is_open == True).order_by(ScheduleManagement.created_date.desc()).all()

    def create_schedule_management(self, schedule_management):
        try:
            self.session.add(schedule_management)
            self.session.commit()
            return schedule_management
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None
            
    
        
        