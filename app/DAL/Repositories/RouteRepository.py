from typing import List
from app.GUI.model.models import Route
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RouteRepository(IRouteRepository):


    def get_routes_all(self, session: Session) -> List[Route]:
        return session.query(Route).all()
    
    def get_routes_by_list_places_id(self, session: Session,list_places_id):
        pass

    def get_route(self, session: Session,route_id: int) -> Route:
        return session.query(Route).get(route_id)
    
    def add_route(self, session: Session,route: Route) -> Route:
        session.add(route)
        return route
    
    def update_route(self, session: Session,route: Route, new_route: Route) -> Route:
        route.route_name = new_route.route_name
        return route

    def delete_route(self, session: Session,route: Route) -> bool:
        session.delete(route)
        return True
