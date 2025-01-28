from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD'))
DB_URL = f'{os.getenv('DB_DRIVER')}://{os.getenv('DB_USERNAME')}:{DB_PASSWORD}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?charset=utf8mb4'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hard to guess key'
    REDIS_URL = os.getenv('REDIS_URL')
    SQLALCHEMY_DATABASE_URI = DB_URL
    # GEVENT_SUPPORT = True
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 15)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30)))

