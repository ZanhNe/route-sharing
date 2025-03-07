from app.GUI.model.models import ScheduleManagement, ScheduleShare, RoadmapShare, Route
from typing import List
from datetime import datetime
from app.BLL.Interfaces.IScheduleManagementService import IScheduleManagementService
from app.DAL.Interfaces.IScheduleManagementRepository import IScheduleManagementRepository
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class ScheduleManagementService(IScheduleManagementService):
    @inject
    def __init__(self, schedule_management_repo: IScheduleManagementRepository, schedule_share_repo: IScheduleShareRepository, tm: TransactionManager):
        self.schedule_management_repo = schedule_management_repo
        self.schedule_share_repo = schedule_share_repo
        self.tm = tm
        

    def get_all_schedule_management(self):
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_all_schedule_management(session=session)
    
    def get_schedule_management_by_title_and_user_id(self, schedule_management_title: str, user_id: str) -> List[ScheduleManagement]:
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_schedule_management_by_title_and_user_id(session=session, schedule_management_title=schedule_management_title, user_id=user_id)

    def get_schedule_management_by_schedule_management_id(self, schedule_management_id: int) -> ScheduleManagement:
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_schedule_management_by_schedule_management_id(session=session, schedule_management_id=schedule_management_id)

    def get_all_schedule_management_by_user_id(self, user_id: int) -> List[ScheduleManagement]:
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_all_schedule_management_by_user_id(session=session, user_id=user_id)
    
    def get_all_schedule_managements_opening(self) -> List[ScheduleManagement]:
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_all_schedule_managements_opening(session=session)

    def get_schedule_management_by_id(self, schedule_management_id):
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_schedule_management_by_id(session=session, schedule_management_id=schedule_management_id)
    
    def get_some_schedule_management_by_ids(self, list_schedule_management_id):
        with self.tm.transaction('') as session:
            return self.schedule_management_repo.get_some_schedule_management_by_ids(session=session, list_schedule_management_id=list_schedule_management_id)
    
    def create_schedule_management(self, schedule_management: ScheduleManagement):
        with self.tm.transaction('Lỗi khi tạo schedule management') as session:
            return self.schedule_management_repo.create_schedule_management(session=session, schedule_management=schedule_management)
    
    def update_schedule_management(self, user_id, schedule_management_id: int, data: dict):
        with self.tm.transaction('Lỗi khi cập nhật schedule management') as session:
            schedule_management = self.schedule_management_repo.get_schedule_management_by_id(session=session, schedule_management_id=schedule_management_id)
            if not schedule_management: 
                raise Exception('Quản lý lịch trình không tồn tại')
            if (user_id != schedule_management.user_id):
                raise Exception('Bạn không có quyền truy cập vào danh sách của người khác')
            schedule_management = self.schedule_management_repo.update_schedule_management(session=session, schedule_management_id=schedule_management_id, data=data)
            return schedule_management
        

    def handle_roadmaps_share(self, schedule_management_id: int, schedule_setup_informations: dict, route: Route) -> List[ScheduleShare]:
        with self.tm.transaction('Lỗi khi xử lý schedule management') as session:
            list_schedules_share = []
            for schedule in schedule_setup_informations['schedules']:
                departure_date_format = datetime.fromisoformat(schedule['date'].split('+')[0])
                schedule_share = self.schedule_share_repo\
                    .get_schedule_share_by_departure_date(session=session, departure_date=departure_date_format\
                                                                            , schedule_management_id=schedule_management_id)
                if (not schedule_share):
                    schedule_share = ScheduleShare(departure_date=datetime.fromisoformat(schedule['date']), schedule_management_id=schedule_management_id)
                    schedule_share = self.schedule_share_repo.create_schedule_share(session=session, schedule_share=schedule_share)
                    session.flush()
                schedule_share.logAllRoadmaps()
                if (not schedule_share.checkValidRoadmapFromAnotherTime(schedule['times'][0]['departureTime'].split('+')[0])):
                    raise Exception(f'Thời gian bắt đầu của lộ trình mới phải sau thời gian kết thúc của lộ trình ngày: {schedule_share.list_roadmaps[-1].estimated_arrival_time}')
                list_roadmaps = []
                for times in schedule['times']:
                    roadmap_share = RoadmapShare(estimated_departure_time=datetime.fromisoformat(times['departureTime'])\
                                                 , estimated_arrival_time=datetime.fromisoformat(times['arrivalTime'])\
                                                , schedule_share_id=schedule_share.id, route_id=route.route_id)
                    list_roadmaps.append(roadmap_share)
                schedule_share = self.schedule_share_repo.add_roadmaps_share_to_schedule_share(session=session, schedule_share=schedule_share, list_roadmap=list_roadmaps)
                session.flush()
                list_schedules_share.append(schedule_share)
            return list_schedules_share
        
