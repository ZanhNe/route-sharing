from app.BLL.Interfaces.IUserService import IUserService
from app.DAL.Interfaces.IUserRepository import IUserRepository
from typing import List
from app.GUI.model.models import User


class UserService(IUserService):
    def __init__(self, userRepository: IUserRepository):
        self.userRepository = userRepository

    def get_user_all(self) -> List[User]:
        return self.userRepository.get_user_all(), 200
    
    def get_user_by_id(self, user_id: int) -> User:
        return self.userRepository.get_user_by_id(user_id=user_id)
    
    def get_user_by_account(self, user_account: str) -> User:
        result = self.userRepository.get_user_by_account(user_account=user_account)
        if (not result):
            return {'error': 'User not found'}, 404
        return result, 200
    
    def add_user(self, user: User) -> User:
        user = self.userRepository.add_user(user=user)
        if (not user):
            return None
        return user
    
    def update_status_user(self, new_status: str, user: User) -> User:
        return self.userRepository.update_status_user(new_status=new_status, user=user)
    

    def update_status_user_request(self, main_user_id_accept: int, secondary_user_id_accept: int, list_declined_user_id: List[int]):
        return self.userRepository.update_status_user_request(main_user_id_accept=main_user_id_accept, secondary_user_id_accept=secondary_user_id_accept, list_declined_user_id=list_declined_user_id)