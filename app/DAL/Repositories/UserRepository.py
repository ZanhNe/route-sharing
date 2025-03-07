from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.GUI.model.models import User
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

class UserRepository(IUserRepository): 

    def get_user_all(self, session: Session) -> List[User]:
        return session.query(User).all()

    def get_user_by_id(self, session: Session, user_id: str) -> User:
        return session.query(User).get(user_id)
    
    def get_user_by_account(self, session: Session, user_account: str) -> User:
        return session.query(User).filter(User.user_account == user_account).first()
    
    def add_user(self, session: Session, user: User) -> User:
        session.add(user)
        return user
    
        
    def update_user(self, session: Session, user_id: str, payloads: dict) -> User:
        session.query(User).filter(User.user_id == user_id).update(values=payloads)
        return session.query(User).get(ident=user_id)
    
    def delete_user(self, session: Session, user_id):
        session.query(User).filter(User.user_id == user_id).delete()

        

        
    
        
    
    
