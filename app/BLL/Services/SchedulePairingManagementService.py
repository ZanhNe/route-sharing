from typing import List
from app.GUI.model.models import SchedulePairingManagement
from app.BLL.Interfaces.ISchedulePairingManagementService import ISchedulePairingManagementService
from app.DAL.Interfaces.ISchedulePairingManagementRepository import ISchedulePairingManagementRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError 

class SchedulePairingManagementService(ISchedulePairingManagementService):

    def __init__(self, schedule_management_repository: ISchedulePairingManagementRepository):
        self.schedule_management_repository = schedule_management_repository

    def get_schedule_pairing_management_of_user(self, session: Session, user_id):
        try:
            schedule_pairing_management = self.schedule_management_repository.get_schedule_pairing_management_of_user(session=session, user_id=user_id)
            if not schedule_pairing_management:
                schedule_pairing_management_raw = SchedulePairingManagement(user_id=user_id)
                schedule_pairing_management = self.schedule_management_repository\
                                            .create_schedule_pairing_management_of_user(session=session, schedule_pairing_management=schedule_pairing_management_raw)
            session.commit()
            return schedule_pairing_management
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise Exception('Lỗi khi tạo schedule pairing management')
        finally: 
            session.close()