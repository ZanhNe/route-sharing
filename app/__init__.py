from flask import Flask
from .extentions.extentions import custom_init_app, create_db
# from app.GUI.controller.auth_routes import auth_bp
from app.GUI.controller.role_routes import role_bp
from app.GUI.controller.user_routes import user_bp
# from app.GUI.controller.location_routes import location_bp
# from app.GUI.controller.user_role_routes import user_role_bp
# from app.GUI.controller.user_location_routes import user_location_bp
# from app.GUI.controller.user_route_routes import user_route_bp
# from app.GUI.controller.route_routes import route_bp
# from app.GUI.controller.route_location_routes import route_location_bp
from app.GUI.controller.find_place_routes import find_places_bp
from app.GUI.controller.place_routes import place_route_bp
# from app.GUI.controller.user_share_routes import route_share_bp
from app.GUI.controller.noti_routes import notification_route_bp
# from app.GUI.controller.request_match_routes import request_match_bp
from app.GUI.controller.conversation_routes import conversation_route_bp
from app.GUI.controller.schedule_management_routes import schedule_management_bp
from app.GUI.controller.test_routes import test_bp
from config import Config






def create_db_init():
    create_db()
    print("Succesful")

def create_app():
    app = Flask(__name__)
    app.config.from_object(obj=Config)
    custom_init_app(app=app)
    app.register_blueprint(role_bp)
    app.register_blueprint(user_bp)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(location_bp)
    # app.register_blueprint(user_location_bp)
    # app.register_blueprint(user_role_bp)
    # app.register_blueprint(user_route_bp)
    # app.register_blueprint(route_bp)
    # app.register_blueprint(route_location_bp)
    app.register_blueprint(find_places_bp)
    app.register_blueprint(place_route_bp)
    # app.register_blueprint(route_share_bp)
    app.register_blueprint(notification_route_bp)
    # app.register_blueprint(request_match_bp)
    app.register_blueprint(conversation_route_bp)
    app.register_blueprint(schedule_management_bp)
    app.register_blueprint(test_bp)
    return app