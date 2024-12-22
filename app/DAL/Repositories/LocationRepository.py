from app.GUI.model.models import Location
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.DAL.Interfaces.ILocationRepository import ILocationRepository

class LocationRepository(ILocationRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_locations_all(self) -> List[Location]:
        return self.session.query(Location).all()
    
    def get_location(self, location_id: int) -> Location:
        try: 
            location = self.session.query(Location).get(ident=location_id)
            if (not location):
                raise Exception('Location not found')
            return location
        except Exception as e:
            print(e)
            return None
        
    def get_location_by_address(self, location_address: str) -> Location:
        try:
            location = self.session.query(Location).filter(Location.address == location_address).first()
            print(location)
            if (not location):
                raise Exception('Location not found')
            return location
        except Exception as e:
            print(e)
            return None
    
    def get_locations_by_address(self, list_address: List[str]) -> List[Location]:
        return self.session.query(Location).filter(Location.address.in_(list_address)).all()

    
    def add_location(self, location: Location) -> Location:
        try:
            self.session.add(location)
            self.session.commit()
            return location
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
    
    def update_location(self, location_id: int, new_location: Location) -> Location:
        try:
            location = self.get_location(location_id=location_id)
            if location:
                location['address'] = new_location['address']
                location['latitude'] = new_location['latitude']
                location['longitude'] = new_location['longitude']
                location['routes'] = new_location['routes']
                location['users'] = new_location['users']

                self.session.commit()

            return location 
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
            return None
    
    def delete_location(self, location_id: int) -> bool:
        try: 
            location = self.get_location(location_id=location_id)
            if (not location):
                raise Exception('Location not found')
            self.session.delete(location)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(e)
        except Exception as e:
            print(e)
        finally:
            return False