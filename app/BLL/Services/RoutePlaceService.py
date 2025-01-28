from typing import List
# from app.custom.Functions import get_coordinate
from app.GUI.model.models import Route, Place
from app.DAL.Interfaces.IRoutePlaceRepository import IRoutePlaceRepository
from app.DAL.Interfaces.IPlaceRepository import IPlaceRepository
from app.DAL.Interfaces.IRouteRepository import IRouteRepository
from app.BLL.Interfaces.IRoutePlaceService import IRoutePlaceService

class RoutePlaceService(IRoutePlaceService):
    def __init__(self, route_place_repository: IRoutePlaceRepository, place_repository: IPlaceRepository, route_repository: IRouteRepository) -> None:
        self.route_place_repository = route_place_repository
        self.place_repository = place_repository
        self.route_repository = route_repository

    def add_place_to_route(self, route: Route, list_places: List[Place]) -> Route:
        route = self.route_place_repository.add_place_to_route(route=route, list_places=list_places)
        if (not route):
            return None
        return route
    
    def handle_new_route(self, route_name: str, list_places: List[Place]) -> Route:
        try:
            new_route = Route(route_name=route_name) #TH2 : Chưa có route trong DB --> Tạo route mới 
            route_after_add = self.route_repository.add_route(route=new_route)
            if (not route_after_add):
                return None
            return self.add_place_to_route(route=route_after_add, list_places=list_places)
        except Exception as e:
            print(e)
            return None
    
    def get_route_with_place(self, route_name: str, list_place_id: List[str]) -> Route:
        routes = self.route_repository.get_routes_all()
        list_places = self.place_repository.get_places_by_list_id(list_place_id=list_place_id)


        for route in routes: #Nếu statement trên không execute thì có 2 TH : TH1 là đã có route trong DB vì 2 location kia đã tạo --> Duyệt trong Route tìm route
            flag = True
            if (len(route.places) == len(list_places)):
                for place1, place2 in zip(route.places, list_places):
                    if (place1.place_id != place2.place_id):
                        flag = False
                        break
                if (flag == True):
                    print(route.places[0].formatt_address)
                    print(route.places[1].formatt_address)
                    return route
                
                
        
        #Nếu duyệt hết routes mà không có route tương ứng thì tạo route mới     
        return self.handle_new_route(route_name=route_name, list_places=list_places) 
        



    
