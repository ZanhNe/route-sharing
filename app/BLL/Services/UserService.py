from app.BLL.Interfaces.IUserService import IUserService
from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from typing import List
from app.GUI.model.models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from injector import inject

class UserService(IUserService):
    @inject
    def __init__(self, user_repository: IUserRepository, role_repository: IRoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def get_user_all(self, session: Session) -> List[User]:
        return self.user_repository.get_user_all(session=session), 200
    
    def get_user_by_id(self, session: Session, user_id: str) -> User:
        return self.user_repository.get_user_by_id(session=session, user_id=user_id)
    
    def get_user_by_account(self, session: Session, user_account: str) -> User:
        result = self.user_repository.get_user_by_account(session=session, user_account=user_account)
        if (not result):
            raise Exception('Không tìm thấy user')
        return result
    

    def add_user(self, session: Session, user: User) -> User:
        try:
            user_role = self.role_repository.get_role_by_name(role_name="USER")
            user.roles.append(user_role)
            user = self.user_repository.add_user(session=session, user=user)
            session.commit()
            return user
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise Exception('Lỗi khi thêm user vào Database')
        finally:
            session.close()
    
    def update_user(self, session: Session, user):
        try:
            user = self.user_repository.update_user(user=user)
            session.commit()
            return user
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
            raise Exception('Lỗi khi cập nhật user')
        finally:
            session.close()
