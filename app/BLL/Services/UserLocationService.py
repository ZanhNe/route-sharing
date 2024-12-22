from app.BLL.Interfaces.IUserLocationService import IUserLocationService
from app.DAL.Interfaces.IUserLocationRepository import IUserLocationRepository
from app.GUI.model.models import Location, User

class UserLocationService(IUserLocationService):
    def __init__(self, user_location_repository: IUserLocationRepository) -> None:
        self.user_location_repository = user_location_repository

    def add_location_user(self, user: User, location: Location) -> User:
        new_location = self.user_location_repository.add_location_user(user=user, location=location)
        if (not new_location):
            return {'error': 'Vui lòng thử lại, đã có lỗi trong quá trình thêm tọa độ'}, 400
        return new_location, 200
    

        