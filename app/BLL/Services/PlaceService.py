from app.GUI.model.models import Place, Location
from typing import List
from app.BLL.Interfaces.IPlaceService import IPlaceService
from app.DAL.Interfaces.IPlaceRepository import IPlaceRepository

class PlaceService(IPlaceService):

    def __init__(self, place_repository: IPlaceRepository) -> None:
        self.place_repository = place_repository

    def get_place(self, place_id: str) -> Place:
        return self.place_repository.get_place(place_id=place_id)
    
    def get_places_by_list_id(self, list_place_id: List[str]) -> List[Place]:
        return self.place_repository.get_places_by_list_id(list_place_id=list_place_id)
    
    def create_place(self, place: Place, location: Location) -> Place:
        return self.place_repository.create_place(place=place, location=location)
    
    def get_places_by_list_id_include_null(self, list_place_id: List[str]) -> List[Place]:
        return self.place_repository.get_places_by_list_id_include_null(list_place_id=list_place_id)
    