from app.GUI.model.models import ScheduleManagement, ScheduleShare, RoadmapShare, Route
from typing import List
from app.BLL.Interfaces.IScheduleManagementService import IScheduleManagementService
from app.BLL.Interfaces.INotificationService import INotificationService
from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.BLL.Interfaces.IRoutePlaceService import IRoutePlaceService
from app.BLL.Interfaces.IScheduleManagementShareRoute import IScheduleManagementShareRoute
from sqlalchemy.exc import SQLAlchemyError

class ScheduleManagementShareRoute(IScheduleManagementShareRoute):
    def __init__(self, schedule_management_service: IScheduleManagementService, route_place_service: IRoutePlaceService, notification_service: INotificationService, roadmap_request_service: IRoadmapRequestService):
        self.schedule_management_service = schedule_management_service
        self.route_place_service = route_place_service
        self.notification_service = notification_service
        self.roadmap_request_service = roadmap_request_service

    def handle_schedule_share(self, schedule_setup_informations: dict) -> List[ScheduleShare]:
        try:
            route = self.route_place_service.get_route_with_place(list_place_id=schedule_setup_informations['list_place_id'], route_name='')
            list_schedule_shares = self.schedule_management_service.handle_roadmaps_share(schedule_management_id=schedule_setup_informations['scheduleManagement']['id'], schedule_setup_informations=schedule_setup_informations, route=route)

            return list_schedule_shares
        except (Exception, SQLAlchemyError) as e:
            print(e)
            raise e
        
    def add_new_request_roadmap(self, validator: dict, roadmap_share_id: int):
        try:
            roadmap_request = self.roadmap_request_service.get_roadmap_request_by_roadmap_share_id_and_sender_id(roadmap_share_id=roadmap_share_id, sender_id=validator['sender_id'])
            if (roadmap_request):
                raise Exception("Yêu cầu cho lộ trình này đã được tạo, vui lòng không gửi lại")
            route = self.route_place_service.get_route_with_place(list_place_id=validator['list_place_id'], route_name='')
            roadmap_request = self.roadmap_request_service.add_new_roadmap_request(validator=validator, route_id=route.route_id, roadmap_share_id=roadmap_share_id)
            notification = self.notification_service.add_new_notification_request_roadmap_of_user(validator=validator)
            return roadmap_request, notification
        except SQLAlchemyError as e:
            raise e
        except Exception as e:
            raise e

        
