from flask import Flask
from config import Config
from app.GUI.controller.role_routes import role_bp
from app.GUI.controller.user_routes import user_bp
from app.GUI.controller.find_place_routes import find_places_bp
from app.GUI.controller.place_routes import place_route_bp
from app.GUI.controller.noti_routes import notification_route_bp
from app.GUI.controller.conversation_routes import conversation_route_bp
from app.GUI.controller.schedule_management_routes import schedule_management_bp
from app.GUI.controller.schedule_pairing_management_routes import schedule_pairing_management_bp
from app.GUI.controller.auth_firebase_routes import auth_firebase_admin_bp
from app.GUI.controller.test_routes import test_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(obj=Config)
    from celery_entry import celery_init_app
    celery_init_app(app)
    from app.extentions.extentions import custom_init_app
    custom_init_app(app=app)
    app.register_blueprint(role_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(find_places_bp)
    app.register_blueprint(place_route_bp)
    app.register_blueprint(notification_route_bp)
    app.register_blueprint(conversation_route_bp)
    app.register_blueprint(schedule_management_bp)
    app.register_blueprint(schedule_pairing_management_bp)
    app.register_blueprint(auth_firebase_admin_bp)
    app.register_blueprint(test_bp)
    return app


flask_app = create_app()