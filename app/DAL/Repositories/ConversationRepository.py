from app.DAL.Interfaces.IConversationRepository import IConversationRepository
from typing import List
from app.GUI.model.models import Conversation, Message
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

class ConversationRepository(IConversationRepository):
    
    def __init__(self, session: Session):
        self.session = session

    def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        return self.session.query(Conversation).get(ident=conversation_id)

    def get_conversation_by_two_user_id(self, first_user_id: int, second_user_id: int) -> Conversation:
        return self.session.query(Conversation).filter(Conversation.main_user_id == first_user_id, Conversation.secondary_user_id == second_user_id).first()
    
    def create_conversation(self, conversation: Conversation):
        try:
            self.session.add(instance=conversation)
            self.session.commit()
            return conversation
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None
        
    def delete_conversation(self, conversation_id):
        pass

    def add_message_to_conversation(self, message: Message) -> Message:
        try:
            self.session.add(message)
            self.session.commit()
            return message
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None

    # def add_list_members_to_conversation(self, conversation: Conversation, members: List[ConversationMember]):
    #     try:
    #         conversation.members.extend(members)
    #         self.session.commit()
    #     except SQLAlchemyError as e:
    #         print(e)
    #         self.session.rollback()