from app.GUI.model.models import ScheduleManagement, ScheduleShare, RoadmapShare, Route
from typing import List
from datetime import datetime
from app.BLL.Interfaces.IScheduleManagementService import IScheduleManagementService
from app.DAL.Interfaces.IScheduleManagementRepository import IScheduleManagementRepository
from app.DAL.Interfaces.IScheduleShareRepository import IScheduleShareRepository
from app.DAL.Interfaces.IRoadmapShareRepository import IRoadmapShareRepository
from sqlalchemy.exc import SQLAlchemyError

class ScheduleManagementService(IScheduleManagementService):
    def __init__(self, schedule_management_repo: IScheduleManagementRepository, schedule_share_repo: IScheduleShareRepository):
        self.schedule_management_repo = schedule_management_repo
        self.schedule_share_repo = schedule_share_repo
        

    def get_all_schedule_management(self):
        return self.schedule_management_repo.get_all_schedule_management()
    
    def get_schedule_management_by_schedule_management_id(self, schedule_management_id: int) -> ScheduleManagement:
        return self.schedule_management_repo.get_schedule_management_by_schedule_management_id(schedule_management_id=schedule_management_id)

    def get_all_schedule_management_by_user_id(self, user_id: int) -> List[ScheduleManagement]:
        return self.schedule_management_repo.get_all_schedule_management_by_user_id(user_id=user_id)
    
    def get_all_schedule_managements_opening(self) -> List[ScheduleManagement]:
        return self.schedule_management_repo.get_all_schedule_managements_opening()

    def get_schedule_management_by_id(self, schedule_management_id):
        return self.schedule_management_repo.get_schedule_management_by_id(schedule_management_id=schedule_management_id)
    
    def get_some_schedule_management_by_ids(self, list_schedule_management_id):
        return self.schedule_management_repo.get_some_schedule_management_by_ids(list_schedule_management_id=list_schedule_management_id)
    
    def create_schedule_management(self, schedule_management: ScheduleManagement):
        return self.schedule_management_repo.create_schedule_management(schedule_management=schedule_management)
    
    def update_schedule_management(self, schedule_management_id: int, data: dict):
        try:
            return self.schedule_management_repo.update_schedule_management(schedule_management_id=schedule_management_id, data=data)
        except Exception as e:
            print(e)
            raise e

    def handle_roadmaps_share(self, schedule_management_id: int, schedule_setup_informations: dict, route: Route) -> List[ScheduleShare]:
        try:
            list_schedules_share = []
            for schedule in schedule_setup_informations['schedules']:
                schedule_share = self.schedule_share_repo.get_schedule_share_by_departure_date_with_roadmap_open(departure_date=schedule['date'])
                if (not schedule_share):
                    schedule_share = ScheduleShare(departure_date=datetime.fromisoformat(schedule['date']), schedule_management_id=schedule_management_id)
                    schedule_share = self.schedule_share_repo.create_schedule_share(schedule_share=schedule_share)
                schedule_share.logAllRoadmaps()
                if (not schedule_share.checkValidRoadmapFromAnotherTime(schedule['times'][0]['departureTime'])):
                    raise Exception(f'Thời gian bắt đầu của lộ trình mới phải sau thời gian kết thúc của lộ trình ngày: {schedule_share.departure_date}')
                list_roadmaps = []
                for times in schedule['times']:
                    roadmap_share = RoadmapShare(estimated_departure_time=datetime.fromisoformat(times['departureTime'])\
                                                 , estimated_arrival_time=datetime.fromisoformat(times['arrivalTime'])\
                                                , schedule_share_id=schedule_share.id, route_id=route.route_id)
                    list_roadmaps.append(roadmap_share)
                schedule_share = self.schedule_share_repo.add_roadmaps_share_to_schedule_share(schedule_share=schedule_share, list_roadmap=list_roadmaps)
                list_schedules_share.append(schedule_share)
            
            return list_schedules_share
        except (Exception, SQLAlchemyError) as e:
            print(e)
            raise e
