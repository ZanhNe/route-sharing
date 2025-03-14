from abc import ABC, abstractmethod
from app.GUI.model.models import Roles
from typing import List


class IRoleService(ABC):
    @abstractmethod
    def get_roles_all(self) -> List[Roles]:
        pass

    @abstractmethod
    def get_role_by_name(self, role_name: str) -> Roles:
        pass

    @abstractmethod
    def get_list_role(self, roles: List[str]) -> List[Roles]:
        pass

    @abstractmethod
    def check_role(self, role_name: str) -> bool:
        pass

    @abstractmethod
    def add_role(self, role: Roles) -> bool:
        pass

    @abstractmethod
    def delete_role(self, role_name: str):
        pass