from abc import ABC, abstractmethod
from app.GUI.model.models import User, Roles
from typing import List

class IUserRoleRepository(ABC):
    @abstractmethod
    def add_role_user(self, user: User, roles: List[Roles]) -> bool:
        pass