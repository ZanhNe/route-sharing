from typing import List
from app.GUI.model.models import Route
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RouteRepository(IRouteRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_routes_all(self) -> List[Route]:
        return self.session.query(Route).all()
    
    def get_routes_by_list_places_id(self, list_places_id):
        pass

    def get_route(self, route_id: int) -> Route:
        return self.session.query(Route).get(route_id)
    
    def add_route(self, route: Route) -> Route:
        try:
            self.session.add(route)
            self.session.commit()
            return route
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
    
    def update_route(self, route: Route, new_route: Route) -> Route:
        try:
            route.route_name = new_route.route_name
            self.session.commit()
            return route
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None

    def delete_route(self, route: Route) -> bool:
        try: 
            self.session.delete(route)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return False