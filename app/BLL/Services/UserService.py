from app.BLL.Interfaces.IUserService import IUserService
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from typing import List
from app.GUI.model.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.custom.Helper.Helper import TransactionManager
from injector import inject

class UserService(IUserService):
    @inject
    def __init__(self, user_repository: IUserRepository, role_repository: IRoleRepository, tm: TransactionManager):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.tm = tm

    def get_user_all(self) -> List[User]:
        with self.tm.transaction('Lỗi khi lấy các users') as session:
            return self.user_repository.get_user_all(session=session)
    
    def get_user_by_id(self, user_id: str) -> User:
        with self.tm.transaction('Lỗi khi lấy ra user') as session:
            return self.user_repository.get_user_by_id(session=session, user_id=user_id)
    
    def get_user_by_account(self, session: Session, user_account: str) -> User:
        with self.tm.transaction('') as session:
            result = self.user_repository.get_user_by_account(session=session, user_account=user_account)
            if (not result):
                raise Exception('Không tìm thấy user')
            return result
    

    def add_user(self, user: User) -> User:
        with self.tm.transaction('Lỗi khi thêm user') as session:
            user_role = self.role_repository.get_role_by_name(role_name="USER")
            user.roles.append(user_role)
            user = self.user_repository.add_user(session=session, user=user)
            return user
    
    def update_user(self, user):
        with self.tm.transaction('Lỗi khi cập nhật user') as session:
            user = self.user_repository.update_user(session=session, user=user)
            return user
        
