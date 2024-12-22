from app.GUI.model.models import Location, User
from typing import List
from app.BLL.Interfaces.ILocationService import ILocationService
from app.DAL.Interfaces.ILocationRepository import ILocationRepository

class LocationService(ILocationService):
    def __init__(self, locationRepository: ILocationRepository) -> None:
        self.locationRepository = locationRepository

    def get_locations_all(self) -> List[Location]:
        return self.locationRepository.get_locations_all(), 200
    
    def get_location(self, location_id: int) -> Location:
        location = self.locationRepository.get_location(location_id=location_id)
        if (not location):
            return {'error': 'Location not found'}, 404
        return location, 200
    
    def get_location_by_address(self, location_address: str) -> Location:
        location = self.locationRepository.get_location_by_address(location_address=location_address)
        if (not location):
            return {'error': 'Location not found'}, 404
        return location, 200
    
    def get_locations_by_address(self, list_address: List[str]) -> List[Location]:
        return self.get_locations_by_address(list_address=list_address)

    def add_location(self, location: Location) -> Location:
        location = self.locationRepository.add_location(location=location)
        if (not location):
            return {'error': 'Lỗi khi thêm tọa độ'}, 400
        return location, 200
    
    def update_location(self, location_id: int, new_location: Location) -> Location:
        location = self.locationRepository.update_location(location_id=location_id, new_location=new_location)
        if (not location):
            return {'error': 'Lỗi khi sửa tọa độ không tồn tại'}, 404
        return location, 200
    
    def delete_location(self, location_id: int) -> bool:
        flag = self.locationRepository.delete_location(location_id=location_id)
        if (not flag):
            return {'error': 'Lỗi khi xóa tọa độ không tồn tại'}, 404
        return flag, 200