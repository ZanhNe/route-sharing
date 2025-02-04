from app.GUI.model.models import ScheduleManagement, ScheduleShare, RoadmapShare, Route
from typing import List
from app.BLL.Interfaces.IScheduleManagementService import IScheduleManagementService
from app.BLL.Interfaces.INotificationService import INotificationService
from app.BLL.Interfaces.IRoadmapRequestService import IRoadmapRequestService
from app.BLL.Interfaces.IRoutePlaceService import IRoutePlaceService
from app.BLL.Interfaces.IScheduleManagementShareRoute import IScheduleManagementShareRoute
from app.BLL.Interfaces.IScheduleShareService import IScheduleShareService
from app.BLL.Interfaces.ISchedulePairingManagementService import ISchedulePairingManagementService
from app.BLL.Interfaces.IRoadmapShareService import IRoadmapShareService
from app.BLL.Interfaces.ISchedulePairingService import ISchedulePairingService
from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, timezone

class ScheduleManagementShareRoute(IScheduleManagementShareRoute):
    def __init__(self, schedule_management_service: IScheduleManagementService \
                 , route_place_service: IRoutePlaceService, notification_service: INotificationService \
                , roadmap_request_service: IRoadmapRequestService, schedule_share_service: IScheduleShareService \
                , roadmap_share_service: IRoadmapShareService, schedule_pairing_management_service: ISchedulePairingManagementService\
                , schedule_pairing_service: ISchedulePairingService, roadmap_pairing_service: IRoadmapPairingService):
        self.schedule_management_service = schedule_management_service
        self.route_place_service = route_place_service
        self.notification_service = notification_service
        self.roadmap_request_service = roadmap_request_service
        self.schedule_share_service = schedule_share_service
        self.roadmap_share_service = roadmap_share_service
        self.schedule_pairing_management_service = schedule_pairing_management_service
        self.schedule_pairing_service = schedule_pairing_service
        self.roadmap_pairing_service = roadmap_pairing_service

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
        
    def handle_update_schedule_share(self, update_schedule_share_validator: dict, schedule_share_id):
        try:
            schedule_share_check = self.schedule_share_service.get_schedule_share_by_departure_date(departure_date=update_schedule_share_validator['departure_date'])
            if (schedule_share_check):
                raise Exception('Đã tồn tại lịch trình với ngày khởi hành này, vui lòng kiểm tra lại')
            
            update_departure_date_str = update_schedule_share_validator['departure_date'][0:10]
            roadmap_share = self.roadmap_share_service.get_roadmap_share_by_schedule_share_id(schedule_share_id=schedule_share_id)
            
            departure_datetime_roadmap_share_str = str(roadmap_share.estimated_departure_time)
            departure_time_roadmap_share_str = departure_datetime_roadmap_share_str[11:]

            update_departure_datetime_str = f'{update_departure_date_str}T{departure_time_roadmap_share_str}'
            update_departure_datetime = datetime.fromisoformat(update_departure_datetime_str)
            datetime_now = datetime.now()
            print(datetime_now)
            print(update_departure_datetime)

            if (update_departure_datetime < datetime_now + timedelta(hours=1)):
                raise Exception('Thời gian chọn phải cách thời điểm hiện tại ít nhất 1 giờ')
            schedule_share = self.schedule_share_service\
                                .update_schedule_share({'id': schedule_share_id}, {'departure_date': datetime.fromisoformat(update_schedule_share_validator['departure_date'])})
            
            return schedule_share
        except Exception as e:
            raise e
        
    def handle_accept_roadmap_request(self, roadmap_request_id: int, main_user_id: str):
        try:
            roadmap_request = self.roadmap_request_service.get_roadmap_request_by_request_id(roadmap_request_id=roadmap_request_id)
            if (roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != main_user_id):
                raise Exception('User không có quyền truy cập vào tài nguyên của User khác')
            self.roadmap_request_service.update_accept_status_roadmap_request(sender_id=roadmap_request.sender_id, roadmap_share_id=roadmap_request.roadmap_share_id, roadmap_request_id=roadmap_request_id)
            
            

            main_schedule_pairing_management = self.schedule_pairing_management_service\
                                                .get_schedule_pairing_management_of_user(user_id=main_user_id)
            secondary_schedule_pairing_management = self.schedule_pairing_management_service\
                                                    .get_schedule_pairing_management_of_user(user_id=roadmap_request.sender_id)
            main_schedule_pairing = self.schedule_pairing_service\
                            .get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(departure_date=roadmap_request.roadmap_share.schedule_share.departure_date\
                                                                                                                , schedule_pairing_management_id=main_schedule_pairing_management.id)
            secondary_schedule_pairing = self.schedule_pairing_service\
                            .get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(departure_date=roadmap_request.roadmap_share.schedule_share.departure_date\
                                                                                                                 , schedule_pairing_management_id=secondary_schedule_pairing_management.id)
            roadmap_pairing = self.roadmap_pairing_service\
                .create_roadmap_pairing(data={'roadmap_request_id': roadmap_request_id})
            main_schedule_pairing.list_roadmap_pairings.append(roadmap_pairing)
            secondary_schedule_pairing.list_roadmap_pairings.append(roadmap_pairing)
            
            main_schedule_pairing = self.schedule_pairing_service.update_schedule_pairing(schedule_pairing=main_schedule_pairing)
            secondary_schedule_pairing = self.schedule_pairing_service.update_schedule_pairing(schedule_pairing=secondary_schedule_pairing)

            notification_pairing = self.notification_service.add_new_notification_status_request(validator={'receiver_id': roadmap_request.sender_id, 'sender_id': main_user_id, 'content': 'Đã chấp nhận yêu cầu ghép cặp'})
            #Khúc này sẽ tạo các notification cho các user bị declined rồi phát cho họ (tính sau)
            roadmap_requests_of_roadmap_share = self.roadmap_request_service.get_roadmaps_request_by_roadmap_share_id(roadmap_share_id=roadmap_request.roadmap_share_id)
            return roadmap_requests_of_roadmap_share, notification_pairing
        except Exception as e:
            print(e)
            raise e
        
    def handle_declined_roadmap_request(self, roadmap_request_id: int, main_user_id: str):
        try:
            roadmap_request = self.roadmap_request_service.get_roadmap_request_by_request_id(roadmap_request_id=roadmap_request_id)
            if (roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != main_user_id):
                raise Exception('User không có quyền truy cập vào tài nguyên của User khác')
            roadmap_request = self.roadmap_request_service\
                    .update_declined_status_roadmap_request(sender_id=roadmap_request.sender_id, roadmap_request_id=roadmap_request.id)
            return roadmap_request
        except Exception as e:
            print(e)
            raise e
        
            





        
