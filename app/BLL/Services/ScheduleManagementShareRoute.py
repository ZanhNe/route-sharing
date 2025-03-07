from app.GUI.model.models import ScheduleShare, Status, StatusMatch, RoadmapPairing, RoadmapPairingRequest, Notification
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
from app.BLL.Interfaces.IRoadmapPairingRequestService import IRoadmapPairingRequestService

from app.custom.Helper.Helper import TransactionManager
from injector import inject

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, timezone
from pytz import timezone
import pprint

class ScheduleManagementShareRoute(IScheduleManagementShareRoute):
    @inject
    def __init__(self, schedule_management_service: IScheduleManagementService \
                 , route_place_service: IRoutePlaceService, notification_service: INotificationService \
                , roadmap_request_service: IRoadmapRequestService, schedule_share_service: IScheduleShareService \
                , roadmap_share_service: IRoadmapShareService, schedule_pairing_management_service: ISchedulePairingManagementService\
                , schedule_pairing_service: ISchedulePairingService, roadmap_pairing_service: IRoadmapPairingService\
                , roadmap_pairing_request_service: IRoadmapPairingRequestService\
                , tm: TransactionManager):
        self.schedule_management_service = schedule_management_service
        self.route_place_service = route_place_service
        self.notification_service = notification_service
        self.roadmap_request_service = roadmap_request_service
        self.schedule_share_service = schedule_share_service
        self.roadmap_share_service = roadmap_share_service
        self.schedule_pairing_management_service = schedule_pairing_management_service
        self.schedule_pairing_service = schedule_pairing_service
        self.roadmap_pairing_service = roadmap_pairing_service
        self.roadmap_pairing_request_service = roadmap_pairing_request_service
        self.tm = tm

    def handle_schedule_share(self, schedule_setup_informations: dict) -> List[ScheduleShare]:
        with self.tm.transaction('') as session:
            route = self.route_place_service.get_route_with_place(list_place_id=schedule_setup_informations['list_place_id'], route_name='')
            list_schedule_shares = self.schedule_management_service.handle_roadmaps_share(schedule_management_id=schedule_setup_informations['scheduleManagementId'], schedule_setup_informations=schedule_setup_informations, route=route)

            return list_schedule_shares
        
        
    def add_new_request_roadmap(self, validator: dict, roadmap_share_id: int):
        with self.tm.transaction('') as session:
            roadmap_request = self.roadmap_request_service\
                .get_roadmap_request_by_roadmap_share_id_and_sender_id(roadmap_share_id=roadmap_share_id, sender_id=validator['sender_id'])
            if (roadmap_request):
                raise Exception("Yêu cầu cho lộ trình này đã được tạo, vui lòng không gửi lại")
            route = self.route_place_service.get_route_with_place(list_place_id=validator['list_place_id'], route_name='')
            session.flush()

            roadmap_request = self.roadmap_request_service.add_new_roadmap_request(validator=validator, route_id=route.route_id, roadmap_share_id=roadmap_share_id)
            session.flush()

            notification = self.notification_service.add_new_notification_request_roadmap_of_user(validator=validator)
            return roadmap_request, notification
        
        
    def handle_update_schedule_share(self, update_schedule_share_validator: dict, schedule_share_id):
        with self.tm.transaction('') as session:
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
        
        
    def handle_accept_roadmap_request(self, roadmap_request_id: int, main_user_id: str):
        with self.tm.transaction('') as session:
            roadmap_request = self.roadmap_request_service.get_roadmap_request_by_request_id(roadmap_request_id=roadmap_request_id)
            if (roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != main_user_id):
                raise Exception('User không có quyền truy cập vào tài nguyên của User khác')
            self.roadmap_request_service.update_accept_status_roadmap_request(sender_id=roadmap_request.sender_id, roadmap_share_id=roadmap_request.roadmap_share_id, roadmap_request_id=roadmap_request_id)
            
            roadmap_share = self.roadmap_share_service.update_roadmap_share(roadmap_share_id=roadmap_request.roadmap_share_id, data_update={'is_open': False})
            session.flush()
            schedule_share = roadmap_share.schedule_share

            index_rs = 0
            index_ss = 0
            for i in range(len(schedule_share.list_roadmaps)):
                if not schedule_share.list_roadmaps[i].is_open:
                    break
                else: index_rs+=1
            
            if index_rs == len(schedule_share.list_roadmaps) - 1:
                schedule_share.is_open = False
                session.flush()
            
            schedule_management = schedule_share.schedule_management
            for i in range(len(schedule_management.list_schedule_shares)):
                if not schedule_management.list_schedule_shares[i].is_open:
                    break
                else: index_ss+=1

            if index_ss == len(schedule_management.list_schedule_shares) - 1:
                schedule_management.is_open = False
                session.flush()




            main_schedule_pairing_management = self.schedule_pairing_management_service\
                                                .get_schedule_pairing_management_of_user(user_id=main_user_id)
            secondary_schedule_pairing_management = self.schedule_pairing_management_service\
                                                    .get_schedule_pairing_management_of_user(user_id=roadmap_request.sender_id)
            
            session.flush()

            main_schedule_pairing = self.schedule_pairing_service\
                            .get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(departure_date=roadmap_request.roadmap_share.schedule_share.departure_date\
                                                                                                                , schedule_pairing_management_id=main_schedule_pairing_management.id)
            secondary_schedule_pairing = self.schedule_pairing_service\
                            .get_or_create_schedule_pairing_by_departure_date_and_schedule_pairing_management_id(departure_date=roadmap_request.roadmap_share.schedule_share.departure_date\
                                                                                                                 , schedule_pairing_management_id=secondary_schedule_pairing_management.id)
            session.flush()

            roadmap_pairing = self.roadmap_pairing_service\
                .create_roadmap_pairing(data={'roadmap_request_id': roadmap_request_id})
            main_schedule_pairing.list_roadmap_pairings.append(roadmap_pairing)
            secondary_schedule_pairing.list_roadmap_pairings.append(roadmap_pairing)
            
            main_schedule_pairing = self.schedule_pairing_service.update_schedule_pairing(schedule_pairing=main_schedule_pairing)
            secondary_schedule_pairing = self.schedule_pairing_service.update_schedule_pairing(schedule_pairing=secondary_schedule_pairing)

            session.flush()
            eta_time = roadmap_pairing.roadmap_request.roadmap_share.estimated_arrival_time
            from app.tasks.tasks import check_outdate_roadmap_pairing
            vietnam_tz = timezone('Asia/Ho_Chi_Minh')
            check_outdate_roadmap_pairing.apply_async(args=[roadmap_pairing.id], eta=vietnam_tz\
                                                      .localize(dt=eta_time))
            

            notification_pairing = self.notification_service.add_new_notification_status_request(validator={'receiver_id': roadmap_request.sender_id, 'sender_id': main_user_id, 'content': 'Đã chấp nhận yêu cầu ghép cặp'})
            #Khúc này sẽ tạo các notification cho các user bị declined rồi phát cho họ (tính sau)
            roadmap_requests_of_roadmap_share = self.roadmap_request_service.get_roadmaps_request_by_roadmap_share_id(roadmap_share_id=roadmap_request.roadmap_share_id)
            return roadmap_requests_of_roadmap_share, notification_pairing, roadmap_share, schedule_share, schedule_management
        
    def handle_declined_roadmap_request(self, roadmap_request_id: int, main_user_id: str):
        with self.tm.transaction('') as session:
            roadmap_request = self.roadmap_request_service.get_roadmap_request_by_request_id(roadmap_request_id=roadmap_request_id)
            if (roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != main_user_id):
                raise Exception('User không có quyền truy cập vào tài nguyên của User khác')
            roadmap_request = self.roadmap_request_service\
                    .update_declined_status_roadmap_request(sender_id=roadmap_request.sender_id, roadmap_request_id=roadmap_request.id)
            return roadmap_request
        
    def handle_update_roadmap_pairing(self, roadmap_pairing_id: int, user_id, data_update: dict):
        with self.tm.transaction('') as session:
            roadmap_pairing = self.roadmap_pairing_service.update_roadmap_pairing(user_id=user_id, data_update=data_update)
            return roadmap_pairing
        
    def handle_start_roadmap_pairing(self, user_id, roadmap_pairing_id: int):
        with self.tm.transaction('Lỗi khi bắt đầu roadmap pairing') as session:
            roadmap_pairing = self.roadmap_pairing_service.get_in_progress_roadmap_pairings(user_id=user_id)
            if roadmap_pairing:
                raise Exception('Bạn đang trong chuyến đi, vui lòng hoàn thành chuyến đi')
            roadmap_pairing = self.roadmap_pairing_service.get_roadmap_pairing_by_id(roadmap_pairing_id=roadmap_pairing_id)
            if not roadmap_pairing:
                raise Exception('Không tìm thấy roadmap pairing')
            roadmap_pairing_secondary_user = self.roadmap_pairing_service\
                .get_in_progress_roadmap_pairings(user_id=roadmap_pairing.roadmap_request.sender_id)
            if roadmap_pairing_secondary_user:
                raise Exception('User còn lại đang trong chuyến đi, bạn vui lòng chờ user hoàn thành')
            #Xử lý roadmap pairing request cho 2 user , nếu trước đó A nhận/gửi request đi sớm cho nhiều người khác --> về mặc định
            #                                           B tương tự
            roadmaps_pairing_request = self.roadmap_pairing_request_service.get_roadmaps_pairing_request_by_user_id(user_id=user_id)
            self.roadmap_pairing_request_service.update_roadmaps_pairing_request_by_user_id(user_id=user_id, data_update={'status': Status.CANCELLED})
            session.flush()
            
            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)
            
            self.roadmap_pairing_service.update_roadmaps_pairing(user_id=user_id, roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})
            session.flush()

            roadmaps_pairing_request_receive_main_user = self.roadmap_pairing_request_service\
                                                        .get_roadmaps_pairing_request_by_secondary_user(secondary_user=user_id)
            self.roadmap_pairing_request_service\
                .update_roadmaps_pairing_request_secondary_user(secondary_user_id=user_id, data_update={'status': Status.CANCELLED})
            
            session.flush()

            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request_receive_main_user:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)
            self.roadmap_pairing_service.update_roadmaps_pairing_secondary_user(roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})

            session.flush()
            
            secondary_user_id = roadmap_pairing.roadmap_request.sender_id
            
            roadmaps_pairing_request = self.roadmap_pairing_request_service.get_roadmaps_pairing_request_by_user_id(user_id=secondary_user_id)
            self.roadmap_pairing_request_service.update_roadmaps_pairing_request_by_user_id(user_id=secondary_user_id, data_update={'status': Status.CANCELLED})
            session.flush()

            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)

            self.roadmap_pairing_service.update_roadmaps_pairing(user_id=secondary_user_id, roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})
            session.flush()


            roadmaps_pairing_request_receive_secondary_user = self.roadmap_pairing_request_service\
                                                        .get_roadmaps_pairing_request_by_secondary_user(secondary_user=secondary_user_id)
            self.roadmap_pairing_request_service\
                .update_roadmaps_pairing_request_secondary_user(secondary_user_id=secondary_user_id, data_update={'status': Status.CANCELLED})
            
            session.flush()

            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request_receive_secondary_user:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)
            self.roadmap_pairing_service.update_roadmaps_pairing_secondary_user(roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})

            session.flush()

            roadmap_pairing_after = self.roadmap_pairing_service\
                        .update_roadmap_pairing(user_id=user_id, roadmap_pairing_id=roadmap_pairing_id, data_update={'status': StatusMatch.IN_PROGRESS, 'actual_departure_time': datetime.now()})
            session.flush()


            departure_date = roadmap_pairing.list_schedule_pairings[0].departure_date
            main_user_roadmaps_pairing = self.roadmap_pairing_service\
                .get_roadmaps_pairing_by_departure_date_and_user_id(user_id=user_id, departure_date=departure_date)
            secondary_user_roadmaps_pairing = self.roadmap_pairing_service\
                .get_roadmaps_pairing_by_departure_date_and_user_id(user_id=secondary_user_id, departure_date=departure_date)
            secondary_user_roadmaps_pairing_request_receive = self.roadmap_pairing_request_service\
                                                                .get_roadmaps_pairing_request_by_secondary_user(secondary_user=secondary_user_id)
            secondary_user_roadmaps_pairing_request_send = self.roadmap_pairing_request_service\
                                                            .get_roadmaps_pairing_request_by_user_id(user_id=secondary_user_id)
            return main_user_roadmaps_pairing\
                , secondary_user_roadmaps_pairing, secondary_user_roadmaps_pairing_request_send\
                    , secondary_user_roadmaps_pairing_request_receive, [user_id, secondary_user_id]


    def handle_end_roadmap_pairing(self, user_id, roadmap_pairing_id: int) -> RoadmapPairing:
        with self.tm.transaction('') as session:
            roadmap_pairing = self.roadmap_pairing_service.get_roadmap_pairing_by_id(roadmap_pairing_id=roadmap_pairing_id)
            if not roadmap_pairing:
                raise Exception('Không tìm thấy Roadmap pairing')
            if roadmap_pairing.status != StatusMatch.IN_PROGRESS:
                raise Exception(f'Roadmap pairing này hiện đang {roadmap_pairing.status}')
            if roadmap_pairing.roadmap_request.sender_id != user_id and roadmap_pairing.roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != user_id:
                raise Exception('Bạn không phải là thành viên của roadmap pairing hiện đang xét, bạn không có quyền')
            if roadmap_pairing.roadmap_request.sender_id == user_id:
                raise Exception('Bạn không phải chủ roadmap pairing, vui lòng liên hệ chủ lộ trình')
            
            roadmap_pairing_after_updated = self.roadmap_pairing_service.update_roadmap_pairing(user_id=user_id, roadmap_pairing_id=roadmap_pairing_id, data_update={'status': StatusMatch.COMPLETED, 'actual_arrival_time': datetime.now()})


            #Tạo notification thông báo cho user còn lại biết (sau)
            return roadmap_pairing_after_updated
        
    def handle_soon_start_roadmap_pairing(self):
        pass


    def send_roadmap_pairing_request(self, sender_id, roadmap_pairing_id: int):
        with self.tm.transaction('Lỗi khi gửi roadmap pairing request') as session:
            roadmap_pairing = self.roadmap_pairing_service.get_in_progress_roadmap_pairings(user_id=sender_id)
            if roadmap_pairing:
                raise Exception('Bạn đang trong chuyến đi, vui lòng hoàn thành chuyến đi')
            roadmap_pairing = self.roadmap_pairing_service.get_roadmap_pairing_by_id(roadmap_pairing_id=roadmap_pairing_id)
            
            if not roadmap_pairing:
                raise Exception('Không tìm thấy roadmap pairing')
            roadmap_pairing_secondary_user = self.roadmap_pairing_service\
                .get_in_progress_roadmap_pairings(user_id=roadmap_pairing.roadmap_request.sender_id)
            if roadmap_pairing_secondary_user:
                raise Exception('User còn lại đang trong chuyến đi, bạn vui lòng chờ user hoàn thành')
            if roadmap_pairing.roadmap_request.roadmap_share.schedule_share.schedule_management.user_id != sender_id:
                raise Exception('Bạn không có quyền gửi đối với lộ trình ghép cặp này')
            if not roadmap_pairing.check_roadmap_pairing_request():
                raise Exception('Người dùng còn lại chưa xác nhận yêu cầu, vui lòng chờ...')
            roadmap_pairing_request = RoadmapPairingRequest(roadmap_pairing_id=roadmap_pairing_id, sender_id=sender_id)
            self.roadmap_pairing_request_service.save_roadmap_pairing_request(roadmap_pairing_request=roadmap_pairing_request)

            roadmap_pairing.status = StatusMatch.WAITING

            notification = self.notification_service\
                .add_new_notification_status_request(validator={'content': 'Một người vừa gửi yêu cầu bắt đầu lộ trình ghép cặp sớm', 'receiver_id': roadmap_pairing.roadmap_request.sender_id, 'sender_id': sender_id})


            return roadmap_pairing_request, notification
        
    def accept_roadmap_pairing_request(self, secondary_user_id, roadmap_pairing_id, roadmap_pairing_request_id):
        with self.tm.transaction('Lỗi khi gửi roadmap pairing request') as session:
            roadmap_pairing_request = self.roadmap_pairing_request_service.get_roadmap_pairing_request_by_id(roadmap_pairing_request_id=roadmap_pairing_request_id)
            if not roadmap_pairing_request_id:
                raise Exception('Không tìm thấy yêu cầu của lộ trình ghép cặp tương ứng')
            roadmap_pairing = roadmap_pairing_request.roadmap_pairing
            if roadmap_pairing.roadmap_request.sender_id == roadmap_pairing_request.sender_id:
                raise Exception('Sự đồng ý phải đến từ người còn lại trong lộ trình ghép cặp')
            if roadmap_pairing.roadmap_request.sender_id != secondary_user_id:
                raise Exception('Bạn không có quyền chấp nhận yêu cầu của lộ trình ghép cặp')
            
            roadmap_pairing_request.status = Status.ACCEPTED
            roadmap_pairing.status = StatusMatch.IN_PROGRESS
            roadmap_pairing.actual_departure_time = datetime.now()
            secondary_user_id = roadmap_pairing.roadmap_request.sender_id
            
            notification = self.notification_service\
                .add_new_notification_status_request(validator={'content': 'Người ghép cặp lộ trình với bạn đã chấp nhận khởi hành sớm', 'receiver_id': roadmap_pairing_request.sender_id, 'sender_id': secondary_user_id})
            session.flush()

            roadmaps_pairing_request = self.roadmap_pairing_request_service.get_roadmaps_pairing_request_by_user_id(user_id=roadmap_pairing_request.sender_id)
            self.roadmap_pairing_request_service.update_roadmaps_pairing_request_by_user_id(user_id=roadmap_pairing_request.sender_id, data_update={'status': Status.CANCELLED})
            
            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)
            
            self.roadmap_pairing_service.update_roadmaps_pairing(user_id=roadmap_pairing_request.sender_id, roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})

            session.flush()


            roadmaps_pairing_request_receive_main_user = self.roadmap_pairing_request_service\
                                                        .get_roadmaps_pairing_request_by_secondary_user(secondary_user_id=roadmap_pairing_request.sender_id)
            self.roadmap_pairing_request_service\
                .update_roadmaps_pairing_request_secondary_user(secondary_user_id=roadmap_pairing_request.sender_id, data_update={'status': Status.CANCELLED})
            

            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request_receive_main_user:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)
            self.roadmap_pairing_service.update_roadmaps_pairing_secondary_user(roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})

            session.flush()
        
            
            roadmaps_pairing_request = self.roadmap_pairing_request_service.get_roadmaps_pairing_request_by_user_id(user_id=secondary_user_id)
            self.roadmap_pairing_request_service.update_roadmaps_pairing_request_by_user_id(user_id=secondary_user_id, data_update={'status': Status.CANCELLED})

            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)

            self.roadmap_pairing_service.update_roadmaps_pairing(user_id=secondary_user_id, roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})
            session.flush()


            roadmaps_pairing_request_receive_secondary_user = self.roadmap_pairing_request_service\
                                                        .get_roadmaps_pairing_request_by_secondary_user(secondary_user_id=secondary_user_id)
            self.roadmap_pairing_request_service\
                .update_roadmaps_pairing_request_secondary_user(secondary_user_id=secondary_user_id, data_update={'status': Status.CANCELLED})

            roadmap_pairing_ids = []
            for roadmap_pairing_request in roadmaps_pairing_request_receive_secondary_user:
                roadmap_pairing_ids.append(roadmap_pairing_request.roadmap_pairing_id)
            self.roadmap_pairing_service.update_roadmaps_pairing_secondary_user(roadmap_pairing_ids=roadmap_pairing_ids, data_update={'status': StatusMatch.NOT_STARTED})

            session.flush()


            return roadmap_pairing, notification
            
    def decline_roadmap_pairing_request(self, secondary_user_id, roadmap_pairing_request_id):
        with self.tm.transaction('Lỗi khi từ chối yêu cầu khởi hành sớm') as session:
            roadmap_pairing_request = self.roadmap_pairing_request_service.get_roadmap_pairing_request_by_id(roadmap_pairing_request_id=roadmap_pairing_request_id)
            if not roadmap_pairing_request_id:
                raise Exception('Không tìm thấy yêu cầu của lộ trình ghép cặp tương ứng')
            roadmap_pairing = roadmap_pairing_request.roadmap_pairing
            if roadmap_pairing.roadmap_request.sender_id == roadmap_pairing_request.sender_id:
                raise Exception('Sự từ chối phải đến từ người còn lại trong lộ trình ghép cặp')
            if roadmap_pairing.roadmap_request.sender_id != secondary_user_id:
                raise Exception('Bạn không có quyền từ chối yêu cầu của lộ trình ghép cặp')
            roadmap_pairing_request.status = Status.ACCEPTED
            roadmap_pairing.status = StatusMatch.NOT_STARTED
            notification = Notification(content='Người còn lại trong phiên lộ trình ghép đã từ chối khởi hành sớm', main_user_id=roadmap_pairing_request.sender_id, secondary_user_id=secondary_user_id)

            return roadmap_pairing, notification




        
    def check_outdate_schedule_share(self):
        with self.tm.transaction('Lỗi khi kiểm tra outdate của schedule share') as session:
            self.roadmap_share_service.check_outdate_roadmaps_share()
            self.schedule_share_service.check_outdate_schedule()

    

        

            



        
