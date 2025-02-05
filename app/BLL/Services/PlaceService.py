from app.GUI.model.models import Place, Location
from typing import List
from app.BLL.Interfaces.IPlaceService import IPlaceService
from app.DAL.Interfaces.IPlaceRepository import IPlaceRepository
from sqlalchemy.orm import Session
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class PlaceService(IPlaceService):
    @inject
    def __init__(self, place_repository: IPlaceRepository, tm: TransactionManager) -> None:
        self.place_repository = place_repository
        self.tm = tm

    def get_place(self, place_id: str) -> Place:
        with self.tm.transaction('') as session:
            return self.place_repository.get_place(session=session, place_id=place_id)


    def get_places_by_list_id(self, list_place_id: List[str]) -> List[Place]:
        with self.tm.transaction('') as session:    
            return self.place_repository.get_places_by_list_id(session=session, list_place_id=list_place_id)
    
    def create_place(self, place: Place, location: Location) -> Place:
        with self.tm.transaction('Lỗi khi tạo place') as session:
            return self.place_repository.create_place(session=session, place=place, location=location)
    
    def get_places_by_list_id_include_null(self, list_place_id: List[str]) -> List[Place]:
        with self.tm.transaction('') as session:
            return self.place_repository.get_places_by_list_id_include_null(session=session, list_place_id=list_place_id)
    