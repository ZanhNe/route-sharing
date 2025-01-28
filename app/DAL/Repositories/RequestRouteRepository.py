# from app.DAL.Interfaces.IRequestRouteRepository import IRequestRouteRepository
# from typing import List
# from app.GUI.model.models import RequestRoute, User, Route, Status
# from sqlalchemy.orm import Session
# from sqlalchemy import and_
# from sqlalchemy.sql import text
# from sqlalchemy.exc import SQLAlchemyError

# class RequestRouteRepository(IRequestRouteRepository):
#     def __init__(self, session: Session):
#         self.session = session

#     def get_requests_route_main_user(self, main_user_id: str) -> List[RequestRoute]:
#         self.session.query(RequestRoute).filter(RequestRoute.main_user_id == main_user_id).all()

#     def get_request_by_request_id(self, request_id: int) -> RequestRoute:
#         return self.session.query(RequestRoute).get(ident=request_id)

#     def get_requests_route_main_user_pending(self, main_user_id: str) -> List[RequestRoute]:
#         return self.session.query(RequestRoute).filter(and_(RequestRoute.main_user_id==main_user_id, RequestRoute.status==Status.PENDING)).all()
    
#     def get_requests_route_secondary_user_pending(self, secondary_user_id: str) -> List[RequestRoute]:
#         return self.session.query(RequestRoute).filter(and_(RequestRoute.secondary_user_id==secondary_user_id, RequestRoute.status==Status.PENDING)).all()

#     def create_request_route(self, main_user: User, secondary_user: User, route: Route) -> RequestRoute:
#         try:
#             new_request_route = RequestRoute(main_user=main_user, secondary_user=secondary_user, route=route)
#             self.session.add(new_request_route)
#             self.session.commit()
#             return new_request_route
#         except SQLAlchemyError as e:
#             print(e)
#             self.session.rollback()
#             return None

#     def get_requests_by_list_request_id(self, list_request_id: List[int]) -> List[RequestRoute]:
#         return self.session.query(RequestRoute).filter(RequestRoute.request_id.in_(list_request_id)).all()
    
    

#     # def update_status_request_route(self, status: str, request_route: RequestRoute) -> RequestRoute:
#     #     # request_route.status = status
#     #     # self.session.commit()
#     #     # return request_route

#     def update_status_accept_request(self, main_user_id: int, request_id: int):
#         try:
#             sql = text("""
#                 update request
#                 set status = case
# 	                when status = 'PENDING' and main_user_id = :main_user_id and request_id <> :request_id then 'DECLINED'
#                     when status = 'PENDING' and request_id = :request_id then 'ACCEPTED'
#                 end
#                 where status = 'PENDING' and main_user_id = :main_user_id
#                 """)
#             params = {'main_user_id': main_user_id, 'request_id': request_id}

#             self.session.execute(sql, params=params)
#             self.session.commit()
#         except SQLAlchemyError as e:
#             print(e)
#             self.session.rollback()

    
            


    
    