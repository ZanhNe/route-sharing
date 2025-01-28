# from app.DAL.Interfaces.IMatchRouteRepository import IMatchRouteRepository
# from typing import List
# from app.GUI.model.models import MatchRoute, User, Route
# from sqlalchemy.orm import Session
# from sqlalchemy import and_
# from sqlalchemy.sql import text
# from sqlalchemy.exc import SQLAlchemyError

# class MatchRouteRepository(IMatchRouteRepository):

#     def __init__(self, session: Session):
#         self.session = session

#     def get_list_match_main_user(self, main_user_id):
#         return self.session.query(MatchRoute).filter(MatchRoute.main_user_id == main_user_id).all()
    
#     def get_list_match_secondary_user(self, secondary_user_id):
#         return self.session.query(MatchRoute).filter(MatchRoute.secondary_user_id == secondary_user_id).all()
    
#     def get_match_route_by_match_id(self, match_route_id):
#         return self.session.query(MatchRoute).get(ident=match_route_id)
    
#     def create_new_match(self, match_route: MatchRoute):
#         try:
#             self.session.add(match_route)
#             self.session.commit()
#             return match_route
#         except SQLAlchemyError as e:
#             print(e)
#             self.session.rollback()
#             return None