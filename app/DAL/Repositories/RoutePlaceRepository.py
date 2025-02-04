from typing import List
from app.DAL.Interfaces.IRoutePlaceRepository import IRoutePlaceRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.GUI.model.models import Place, Route, RouteDetail

class RoutePlaceRepository(IRoutePlaceRepository):


    def add_place_to_route(self, session: Session, route: Route, list_places: List[Place]) -> Route:
        for index, place in enumerate(list_places):
            session.execute(
                RouteDetail.insert().values(
                    route_id = route.route_id,
                    place_id = place.place_id,
                    order = index
                )
            )
        return session.query(Route).filter(Route.route_id == route.route_id).one()

