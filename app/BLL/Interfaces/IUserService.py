from abc import ABC, abstractmethod
from flask import Request
from typing import List
from app.GUI.model.models import User


class IUserService(ABC):

    @abstractmethod
    def get_user_all(self) -> List[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_user_by_account(self, user_account: str) -> User:
        pass

    @abstractmethod
    def add_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user_id, payloads: dict):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    # @abstractmethod
    # def update_status_user(self, new_status: str, user: User) -> User:
    #     pass
