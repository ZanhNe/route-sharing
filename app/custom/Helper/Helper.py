from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class TransactionManager:
    def __init__(self, session: Session):
        self.session = session
    
    @contextmanager
    def transaction(self, error_message: str):
        session = self.session()
        transaction_active = session.in_transaction()

        print('Này test thử transaction: ', transaction_active)

        if not transaction_active:
            session.begin()
        try:
            yield session
            if not transaction_active:
                print('Này đã commit rồi nha')
                session.commit()
        except (SQLAlchemyError, Exception) as e:
            print(e)    
            if not transaction_active:
                session.rollback()
            if isinstance(e, Exception):
                raise e
            elif isinstance(e, SQLAlchemyError):
                raise Exception(error_message)
        
        