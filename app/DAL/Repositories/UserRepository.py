from app.DAL.Interfaces.IUserRepository import IUserRepository
from app.GUI.model.models import User
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session   

    def get_user_all(self) -> List[User]:
        return self.session.query(User).all()

    def get_user_by_id(self, user_id: str) -> User:
        return self.session.query(User).get(user_id)
    
    def get_user_by_account(self, user_account: str) -> User:
        return self.session.query(User).filter(User.user_account == user_account).first()
    
    def add_user(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
        
    def update_status_user(self, new_status: str, user: User) -> User:
        try: 
            user.status = new_status
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return user
        
    def update_user(self, user: User) -> User:
        try:
            self.session.add(instance=user)
            self.session.commit()
            return user
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None
        
    
    def update_status_user_request(self, main_user_id_accept: str, secondary_user_id_accept: str, list_declined_user_id: List[str]):
        try:
            sql = text("""
                    update user
                    set status = case
                        when user_id = :main_user_id_accept or user_id = :secondary_user_id_accept then 'MATCHING'
                        else 'FREE'
                    end
                    where user_id in :list_declined_user_id
                """)
            params = {'main_user_id_accept': main_user_id_accept, 'secondary_user_id_accept': secondary_user_id_accept, 'list_declined_user_id': tuple([main_user_id_accept, secondary_user_id_accept, *list_declined_user_id])}

            self.session.execute(statement=sql, params=params)
            self.session.commit()
            self.session.query(User).filter(User.user_id.in_([secondary_user_id_accept, *list_declined_user_id])).all()
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None
        
    
        
    
    
