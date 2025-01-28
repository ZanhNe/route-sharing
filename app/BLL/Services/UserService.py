from app.BLL.Interfaces.IUserService import IUserService
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from typing import List
from app.GUI.model.models import User


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository, role_repository: IRoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def get_user_all(self) -> List[User]:
        return self.user_repository.get_user_all(), 200
    
    def get_user_by_id(self, user_id: str) -> User:
        return self.user_repository.get_user_by_id(user_id=user_id)
    
    def get_user_by_account(self, user_account: str) -> User:
        result = self.user_repository.get_user_by_account(user_account=user_account)
        if (not result):
            return {'error': 'User not found'}, 404
        return result, 200
    
    

    def add_user(self, user: User) -> User:
        user_role = self.role_repository.get_role_by_name(role_name="USER")
        user.roles.append(user_role)
        user = self.user_repository.add_user(user=user)
        if (not user):
            return None
        return user
    
    def update_status_user(self, new_status: str, user: User) -> User:
        return self.user_repository.update_status_user(new_status=new_status, user=user)
    
    def update_user(self, user):
        return self.user_repository.update_user(user=user)

    def update_status_user_request(self, main_user_id_accept: str, secondary_user_id_accept: str, list_declined_user_id: List[str]):
        return self.user_repository.update_status_user_request(main_user_id_accept=main_user_id_accept, secondary_user_id_accept=secondary_user_id_accept, list_declined_user_id=list_declined_user_id)