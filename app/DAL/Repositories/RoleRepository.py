from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from typing import List
from app.GUI.model.models import Roles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class RoleRepository(IRoleRepository):

    def get_roles_all(self, session: Session) -> List[Roles]:
        return session.query(Roles).all()
    
    def get_role_by_name(self, session: Session,role_name: str) -> Roles:
        return session.query(Roles).filter(Roles.role_name == role_name).first()
    
    def get_list_role(self, session: Session,roles: List[str]) -> List[Roles]:
        return session.query(Roles).filter(Roles.role_name.in_(roles)).all()

    def add_role(self, session: Session,role: Roles) -> Roles:
        session.add(role)
        return role



    
    def check_role(self, session: Session,role_name: str) -> bool:
        search_role = self.get_role_by_name(role_name=role_name)
        if (not search_role):
            return False
        return True
    
    def delete_role(self, session: Session,role_name: str) -> bool:
        # role = self.get_role_by_name(role_name=role_name)
        # if (not role):
        #     return False
        # session.delete(role)
        # session.commit()
        # return True
        session.query(Roles).filter(Roles.role_name == role_name).delete()
    