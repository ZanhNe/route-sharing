from typing import List
from app.DAL.Interfaces.IUserRouteRepository import IUserRouteRepository
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from app.GUI.model.models import Route, User


class UserRouteRepository(IUserRouteRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_route_to_user(self, user: User, route: Route) -> User:
        try:
            user.routes.append(route)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
    
    def get_user_routes(self, user: User) -> List[Route]:
        pass


