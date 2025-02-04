from app.DAL.Interfaces.IPlaceRepository import IPlaceRepository
from typing import List
from app.GUI.model.models import Place, Location
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import literal_column, union_all, select
import pprint

class PlaceRepository(IPlaceRepository):

    def get_place(self, session: Session, place_id: str) -> Place:
        return session.query(Place).get(ident=place_id)
    
    def get_places_by_list_id(self, session: Session, list_place_id: List[str]) -> List[Place]:
        list_tuple_place_id = []
        for index, place_id in enumerate(list_place_id):
            list_tuple_place_id.append((place_id, index + 1))
        temp_table = union_all(
        *[select(literal_column(f"'{place_id}'").label("place_id"), literal_column(f"{pos}").label("pos"))
            for place_id, pos in list_tuple_place_id]
            ).alias("desired_order")
        query = session.query(Place).select_from(temp_table.join(Place, temp_table.c.place_id == Place.place_id)).order_by(literal_column('desired_order.pos'))        
        # query = session.query(Place).filter(Place.place_id.in_(list_place_id))
        # print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
        return query.all()
    
    def get_places_by_list_id_include_null(self, session: Session, list_place_id: List[str]) -> List[Place]:
        list_tuple_place_id = []
        for index, place_id in enumerate(list_place_id):
            list_tuple_place_id.append((place_id, index + 1))
        temp_table = union_all(
        *[select(literal_column(f"'{place_id}'").label("place_id"), literal_column(f"{pos}").label("pos"))
            for place_id, pos in list_tuple_place_id]
            ).alias("desired_order")

        query = session.query(literal_column('desired_order.pos'), Place).select_from(temp_table.outerjoin(Place, temp_table.c.place_id == Place.place_id)).order_by(literal_column('desired_order.pos'))

        # print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
        results = query.all()

        final_results = [row[1] for row in results]

        return final_results

    def create_place(self, session: Session, place: Place, location: Location) -> Place:
        place.location = location
        session.add_all([place, location])
        return place

        
    