from typing import List
from app.GUI.model.models import UserRouteShare, User, Route
from app.DAL.Interfaces.IRouteShareRepository import IRouteShareRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RouteShareRepository(IRouteShareRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_routes_share(self) -> List[UserRouteShare]:
        return self.session.query(UserRouteShare).all()
    
    def get_route_share(self, route_share_id: int) -> UserRouteShare:
        return self.session.query(UserRouteShare).get(ident=route_share_id)
    
    def get_all_routes_share_is_not_match(self) -> List[UserRouteShare]:
        return self.session.query(UserRouteShare).filter(UserRouteShare.is_matched == False).all()
    
    def add_route_share(self, route_share: UserRouteShare, user: User, route: Route) -> UserRouteShare:
        try:
            route_share.user = user
            route_share.route = route
            self.session.add(instance=route_share)
            self.session.commit()
            return route_share
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None