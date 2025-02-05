from abc import ABC, abstractmethod
from flask import Request
from typing import List
from app.GUI.model.models import User
from sqlalchemy.orm import Session

class IUserService(ABC):

    @abstractmethod
    def get_user_all(self, session: Session) -> List[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, session: Session, user_id: str) -> User:
        pass

    @abstractmethod
    def get_user_by_account(self, session: Session, user_account: str) -> User:
        pass

    @abstractmethod
    def add_user(self, session: Session, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, session: Session, user: User) -> User:
        pass

    # @abstractmethod
    # def update_status_user(self, session: Session, new_status: str, user: User) -> User:
    #     pass
