from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase
# from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from opencage.geocoder import OpenCageGeocode
import openrouteservice as ors
from flask_cors import CORS
from here_location_services import LS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from app.Socket.controllers.socket import socketio
from app.GUI.model.models import db
from app.lib.lib_ma import ma
# class Base(DeclarativeBase):
#     pass

load_dotenv()

# db = SQLAlchemy(model_class=Base)
# ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()

key_geocoder = os.getenv('GEOCODER_API_KEY')
key_ors = os.getenv('ORS_API_KEY')
key_here_maps = os.getenv('HERE_MAPS_API_KEY')
key_goong = os.getenv('GOONG_API_KEY')


geocoder = OpenCageGeocode(key=key_geocoder)
client = ors.Client(key=key_ors)
ls = LS(api_key=key_here_maps)





@jwt.user_identity_loader
def user_identity_lookup(user):
    roles = [role.role_name for role in user.roles]
    new_user = {"user_id": user.user_id, "user_name": user.user_name, "roles": roles}
    return new_user



def create_db():
    db.create_all()

def custom_init_app(app) -> None:
    db.init_app(app=app)
    ma.init_app(app=app)
    bcrypt.init_app(app=app)
    jwt.init_app(app=app)
    cors.init_app(app=app, resources={r'/*': {
        'origins': ['http://localhost:5173'],
    }})
    socketio.init_app(app=app, cors_allowed_origins=["http://localhost:5173"])
    migrate.init_app(app=app, db=db)

