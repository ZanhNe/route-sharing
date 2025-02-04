from app.GUI.model.models import Location
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.DAL.Interfaces.ILocationRepository import ILocationRepository

class LocationRepository(ILocationRepository):
    

    def get_locations_all(self, session: Session) -> List[Location]:
        return session.query(Location).all()
    
    def get_location(self, session: Session, location_id: int) -> Location:
        location = session.query(Location).get(ident=location_id)
        return location

        
    def get_location_by_address(self, session: Session, location_address: str) -> Location:
        location = session.query(Location).filter(Location.address == location_address).first()
        return location
    
    def get_locations_by_address(self, session: Session, list_address: List[str]) -> List[Location]:
        return session.query(Location).filter(Location.address.in_(list_address)).all()

    
    def add_location(self, session: Session, location: Location) -> Location:
        session.add(location)
        return location

    
    def update_location(self, session: Session, location_id: int, new_location: Location) -> Location:
        query = session.query(Location).filter(Location.location_id == location_id)
        query.update({'address': new_location['address'], 'latitude': new_location['latitude'], 'longitude': new_location['longitude'], 'routes': new_location['routes'], 'users': new_location['users']})
        location = query.first()
        return location 

    
    def delete_location(self, session: Session, location_id: int) -> bool:
        # try: 
        #     location = self.get_location(location_id=location_id)
        #     if (not location):
        #         raise Exception('Location not found')
        #     session.delete(location)
        #     session.commit()
        #     return True
        # except SQLAlchemyError as e:
        #     session.rollback()
        #     print(e)
        # except Exception as e:
        #     print(e)
        # finally:
        #     return False
        pass