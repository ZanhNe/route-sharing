from typing import List
from app.GUI.model.models import ScheduleManagement
from app.DAL.Interfaces.IScheduleManagementRepository import IScheduleManagementRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class ScheduleManagementRepository(IScheduleManagementRepository):


    def get_schedule_management_by_id(self, session: Session, schedule_management_id: int) -> ScheduleManagement:
        return session.query(ScheduleManagement).get(ident=schedule_management_id)
    
    def get_schedule_management_by_schedule_management_id(self, session: Session, schedule_management_id: int) -> ScheduleManagement:
        return session.query(ScheduleManagement)\
                    .filter(ScheduleManagement.id == schedule_management_id)\
                    .first()
    
    def get_all_schedule_management(self, session: Session):
        return session.query(ScheduleManagement).order_by(ScheduleManagement.created_date.desc()).all()
    
    def get_all_schedule_management_by_user_id(self, session: Session, user_id: int) -> List[ScheduleManagement]:
        return session.query(ScheduleManagement).filter(ScheduleManagement.user_id == user_id).order_by(ScheduleManagement.created_date.desc()).all()

    def get_some_schedule_management_by_ids(self, session: Session, list_schedule_management_id):
        return session.query(ScheduleManagement).filter(ScheduleManagement.id.in_(list_schedule_management_id)).all()

    def get_all_schedule_managements_opening(self, session: Session) -> List[ScheduleManagement]:
        return session.query(ScheduleManagement).filter(ScheduleManagement.is_open == True).order_by(ScheduleManagement.created_date.desc()).all()

    def update_schedule_management(self, session: Session, schedule_management_id: int, data: dict) -> ScheduleManagement:
        session.query(ScheduleManagement).filter(ScheduleManagement.id == schedule_management_id).update(data)
        return session.query(ScheduleManagement).get(ident=schedule_management_id)


    def create_schedule_management(self, session: Session, schedule_management):
        session.add(schedule_management)
        return schedule_management

            
    
        
        