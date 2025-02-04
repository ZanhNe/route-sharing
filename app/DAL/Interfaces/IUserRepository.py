from abc import ABC, abstractmethod
from app.GUI.model.models import User
from typing import List
from sqlalchemy.orm import Session

class IUserRepository(ABC):
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
    
