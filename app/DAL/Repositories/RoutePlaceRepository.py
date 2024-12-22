from typing import List
from app.DAL.Interfaces.IRoutePlaceRepository import IRoutePlaceRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.GUI.model.models import Place, Route, RouteDetail

class RoutePlaceRepository(IRoutePlaceRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_place_to_route(self, route: Route, list_places: List[Place]) -> Route:
        try:
            for index, place in enumerate(list_places):
                self.session.execute(
                    RouteDetail.insert().values(
                        route_id = route.route_id,
                        place_id = place.place_id,
                        order = index
                    )
                )
            self.session.commit()
            return self.session.query(Route).filter(Route.route_id == route.route_id).one()
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
