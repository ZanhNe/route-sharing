# from app.GUI.model.models import User, Route, UserRouteShare
# from typing import List
# from app.BLL.Interfaces.IRouteShareService import IRouteShareService
# from app.DAL.Interfaces.IRouteShareRepository import IRouteShareRepository

# class RouteShareService(IRouteShareService):

#     def __init__(self, route_share_repository: IRouteShareRepository) -> None:
#         self.route_share_repository = route_share_repository

#     def get_all_routes_share(self) -> List[UserRouteShare]:
#         return self.route_share_repository.get_all_routes_share()
    
#     def get_all_routes_share_is_not_match(self) -> List[UserRouteShare]:
#         return self.route_share_repository.get_all_routes_share_is_not_match()
    
#     def get_route_share(self, route_share_id: int) -> UserRouteShare:
#         return self.route_share_repository.get_route_share(route_share_id=route_share_id)
    
#     def add_route_share(self, route_share: UserRouteShare, user: User, route: Route) -> UserRouteShare:
#         return self.route_share_repository.add_route_share(route_share=route_share, user=user, route=route)
