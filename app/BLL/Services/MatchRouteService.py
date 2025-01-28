# from app.GUI.model.models import MatchRoute, User, Route
# from typing import List
# from app.BLL.Interfaces.IMatchRouteService import IMatchRouteService
# from app.DAL.Interfaces.IMatchRouteRepository import IMatchRouteRepository

# class MatchRouteService(IMatchRouteService):
#     def __init__(self, match_route_repository: IMatchRouteRepository):
#         self.match_route_repository = match_route_repository
    
#     def get_list_match_main_user(self, main_user_id: str):
#         return self.match_route_repository.get_list_match_main_user(main_user_id=main_user_id)
    
#     def get_list_match_secondary_user(self, secondary_user_id: str):
#         return self.match_route_repository.get_list_match_secondary_user(secondary_user_id=secondary_user_id)
    
#     def get_match_route_by_match_id(self, match_route_id):
#         return self.match_route_repository.get_match_route_by_match_id(match_route_id=match_route_id)
    
#     def create_new_match(self, main_user: User, secondary_user: User, route: Route):
#         match_route = MatchRoute(main_user=main_user, secondary_user=secondary_user, route=route)
#         return self.match_route_repository.create_new_match(match_route=match_route)
    
    