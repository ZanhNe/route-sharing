from .make_celery import celery_app
from celery.schedules import crontab
from time import sleep
from app.Container.InstanceContainer import injector
from app.BLL.Interfaces.IRoadmapPairingService import IRoadmapPairingService
from app.BLL.Interfaces.IScheduleShareService import IScheduleShareService
from app.BLL.Interfaces.IScheduleManagementShareRoute import IScheduleManagementShareRoute
from app.BLL.Redis.utils.redis_utils import redis_client
import simplejson
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

roadmap_pairing_service = injector.get(interface=IRoadmapPairingService)
schedule_share_service = injector.get(interface=IScheduleShareService)
schedule_management_share_route = injector.get(interface=IScheduleManagementShareRoute)

from dotenv import load_dotenv
import os

load_dotenv()



@celery_app.task
def check_outdate_schedule_share():
    try:
        schedule_management_share_route.check_outdate_schedule_share()
        return 'Kiểm tra thành công'
    except Exception as e:
        return 'Kiểm tra thất bại'




@celery_app.task
def check_outdate_roadmap_pairing(roadmap_pairing_id):
    try:
        roadmap_pairing = roadmap_pairing_service.check_outdate_roadmap_pairing(roadmap_pairing_id=roadmap_pairing_id)
        if roadmap_pairing:
            main_user_id = roadmap_pairing.roadmap_request.roadmap_share.schedule_share.schedule_management.user_id
            secondary_user_id = roadmap_pairing.roadmap_request.sender_id
            payloadsOne = simplejson.dumps(obj={'payload': roadmap_pairing_id, 'send_to': secondary_user_id, 'skip_sid': main_user_id})
            payloadsTwo = simplejson.dumps(obj={'payload': roadmap_pairing_id, 'send_to': main_user_id, 'skip_sid': secondary_user_id})
            
            redis_client.publish('roadmap_pairing.update', payloadsOne)
            redis_client.publish('roadmap_pairing.update', payloadsTwo)
            return 'Success check outdate'
        return 'Nothing to check'
    except Exception as e:
        raise e
    
@celery_app.task
def send_verify_email(EMAIL_RECEIVER: str, LINK: str):
    try:
        # Cấu hình email
        EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Sử dụng App Password, không dùng mật khẩu thật
        msg = EmailMessage()
        msg['Subject'] = 'Email vertification!'
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg.set_content(f'Hello, Follow this link to verify your email address, \
                        link: {LINK}, If you didn’t ask to verify this address, you can ignore this email. Thanks')
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465) as server:
            server.login(user=EMAIL_SENDER, password=EMAIL_PASSWORD)
            server.send_message(msg=msg)
        print("Email sent successfully!")
        return 'Success'
    except Exception as e:
        print('Gửi email thất bại')
        return 'Failed'
