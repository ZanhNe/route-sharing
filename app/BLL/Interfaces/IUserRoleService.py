from abc import ABC, abstractmethod
from app.GUI.model.models import User, Roles

class IUserRoleService(ABC):
    @abstractmethod
    def add_role_user(self, user: User, role: Roles) -> bool:
        pass