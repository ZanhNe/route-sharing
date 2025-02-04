from abc import ABC, abstractmethod
from app.GUI.model.models import Roles
from typing import List
from sqlalchemy.orm import Session
class IRoleRepository(ABC):
    @abstractmethod
    def get_roles_all(self, session: Session) -> List[Roles]:
        pass

    @abstractmethod
    def get_role_by_name(self, session: Session, role_name: str) -> Roles:
        pass

    @abstractmethod
    def add_role(self, session: Session, role: Roles) -> None:
        pass

    @abstractmethod
    def check_role(self, session: Session, role_name: str) -> bool:
        pass

    @abstractmethod 
    def delete_role(self, session: Session, role_name: str) -> bool:
        pass

    