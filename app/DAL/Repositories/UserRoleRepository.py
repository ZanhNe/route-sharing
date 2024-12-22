from app.DAL.Interfaces.IUserRoleRepository import IUserRoleRepository
from typing import List
from app.GUI.model.models import User, Roles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
class UserRoleRepository(IUserRoleRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_role_user(self, user: User, roles: List[Roles]) -> bool:
        try:
            user.roles.extend(roles)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return False