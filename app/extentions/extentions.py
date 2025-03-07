from opencage.geocoder import OpenCageGeocode
import openrouteservice as ors
from flask_cors import CORS
from here_location_services import LS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow
import simplejson
from flask_socketio import SocketIO


#import cloudinary lib
import cloudinary


load_dotenv()

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('CLOUD_API_KEY'),
    api_secret = os.getenv('CLOUD_API_SECRET'),
    secure = True
)

cors = CORS()
migrate = Migrate()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base, session_options={"expire_on_commit": False})
ma = Marshmallow()

socketio = SocketIO(json=simplejson, async_mode='gevent')

key_geocoder = os.getenv('GEOCODER_API_KEY')
key_ors = os.getenv('ORS_API_KEY')
key_here_maps = os.getenv('HERE_MAPS_API_KEY')
key_goong = os.getenv('GOONG_API_KEY')

cred = credentials.Certificate("firebase_admin.json")
firebase_admin.initialize_app(cred)


geocoder = OpenCageGeocode(key=key_geocoder)
client = ors.Client(key=key_ors)
ls = LS(api_key=key_here_maps)





def create_db():
    db.create_all()

def custom_init_app(app) -> None:
    db.init_app(app=app)
    ma.init_app(app=app)
    cors.init_app(app=app, resources={r'/*': {
        'origins': ['http://localhost:5173'],
    }})
    socketio.init_app(app=app, cors_allowed_origins=["http://localhost:5173"])
    migrate.init_app(app=app, db=db)

