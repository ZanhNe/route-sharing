from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from typing import List
from app.GUI.model.models import Roles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RoleRepository(IRoleRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_roles_all(self) -> List[Roles]:
        return self.session.query(Roles).all()
    
    def get_role_by_name(self, role_name: str) -> Roles:
        return self.session.query(Roles).filter(Roles.role_name == role_name).first()
    
    def get_list_role(self, roles: List[str]) -> List[Roles]:
        return self.session.query(Roles).filter(Roles.role_name.in_(roles)).all()

    def add_role(self, role: Roles) -> bool:
        try:
            self.session.add(role)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return False


    
    def check_role(self, role_name: str) -> bool:
        search_role = self.get_role_by_name(role_name=role_name)
        if (not search_role):
            return False
        return True
    
    def delete_role(self, role_name: str) -> bool:
        role = self.get_role_by_name(role_name=role_name)
        if (not role):
            return False
        self.session.delete(role)
        self.session.commit()
        return True
    