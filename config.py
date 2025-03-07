from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
DB_URL = f'{os.getenv('DB_DRIVER')}://{os.getenv('DB_USERNAME')}:{DB_PASSWORD}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4'


class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_CONFIG = {
        'task_serializer': 'json',
        'accept_content': ['json'],
        'result_serializer': 'json',
        'timezone': 'Asia/Ho_Chi_Minh'
    }
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess key'
    REDIS_URL = os.getenv('REDIS_URL')
    SQLALCHEMY_DATABASE_URI = DB_URL
    # SQLALCHEMY_ECHO = True
    # GEVENT_SUPPORT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    DEBUG = os.getenv('DEBUG', 'False') == 'True'


