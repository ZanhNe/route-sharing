from typing import List
from app.GUI.model.models import RoadmapRequest, Status
from app.DAL.Interfaces.IRoadmapRequestRepository import IRoadmapRequestRepository
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class RoadmapRequestRepository(IRoadmapRequestRepository):

    def get_roadmap_request_by_request_id(self, session: Session,roadmap_request_id):
        return session.query(RoadmapRequest).get(ident=roadmap_request_id)
    
    def get_roadmaps_request_by_roadmap_share_id(self, session: Session,roadmap_share_id):
        return session.query(RoadmapRequest).filter(RoadmapRequest.roadmap_share_id == roadmap_share_id).order_by(RoadmapRequest.id.desc()).all()
    
    def get_roadmap_request_by_roadmap_share_id_and_sender_id(self, session: Session,roadmap_share_id, sender_id) -> RoadmapRequest:
        return session.query(RoadmapRequest).filter(RoadmapRequest.roadmap_share_id == roadmap_share_id, RoadmapRequest.sender_id == sender_id).first()

    def update_accept_status_roadmap_request(self, session: Session,sender_id: str, roadmap_request_id: int, roadmap_share_id: int) -> RoadmapRequest:
        queryText1 = text(
                """
                    update roadmap_request
                    set status = case
                        when id = :roadmap_request_id then 'ACCEPTED'
                        else 'DECLINED'
                    end
                    where roadmap_share_id = :roadmap_share_id;
 
                """
            )

        queryText2 = text(
                """
                    update roadmap_request
                    set status = 'DECLINED'
                    where roadmap_share_id in (select * from (select distinct rse.id
                                                from roadmap_share rse join roadmap_request rst 
                                                on rse.id = rst.id 
                                                where rse.id != :roadmap_share_id and rst.sender_id = :sender_id
                                                and ( not (rse.estimated_arrival_time <= (select estimated_departure_time 
                                                                                    from roadmap_share where roadmap_share.id = :roadmap_share_id))
                                                or not (rse.estimated_departure_time >= (select estimated_arrival_time 
                                                                                    from roadmap_share where roadmap_share.id = :roadmap_share_id))
                                                    )
                                                                                     
                                                ) as derived_ids
                                                );
                """
            )
            
        session.execute(queryText1, {'roadmap_request_id': roadmap_request_id, 'roadmap_share_id': roadmap_share_id})
        session.execute(queryText2, {'sender_id': sender_id, 'roadmap_share_id': roadmap_share_id})

        
    def update_declined_status_roadmap_request(self, session: Session,sender_id, roadmap_request_id):
        session.query(RoadmapRequest).filter(RoadmapRequest.sender_id == sender_id, RoadmapRequest.id == roadmap_request_id).update({'status': Status.DECLINED})
        return session.query(RoadmapRequest).get(ident=roadmap_request_id)
        
    
    def get_roadmaps_request_by_sender_id(self, session: Session,sender_id) -> List[RoadmapRequest]:
        return session.query(RoadmapRequest).filter(RoadmapRequest.sender_id == sender_id).order_by(RoadmapRequest.id.desc()).all()

    def create_roadmap_request(self, session: Session,roadmap_request):
        session.add(instance=roadmap_request)
        return roadmap_request
