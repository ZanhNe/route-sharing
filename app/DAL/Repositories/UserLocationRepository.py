from app.DAL.Interfaces.IUserLocationRepository import IUserLocationRepository
from app.GUI.model.models import Location, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class UserLocationRepository(IUserLocationRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def add_location_user(self, user: User, location: Location) -> Location:
        try: 
            user.locations.append(location)
            self.session.commit()
            return location
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None