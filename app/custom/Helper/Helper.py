from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class TransactionManager:
    def __init__(self, session: Session):
        self.session = session
    
    @contextmanager
    def transaction(self):
        transaction_active = self.session.in_transaction()

        if not transaction_active:
            self.session.begin()
        try:
            yield self.session
            if not transaction_active:
                self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            if not transaction_active:
                self.session.rollback()
            raise Exception('Lỗi thực thi DB')
        finally:
            if not transaction_active:
                self.session.close()