from app.DAL.Interfaces.IConversationRepository import IConversationRepository
from typing import List
from app.GUI.model.models import Conversation, Message, Participant, User
from sqlalchemy.orm import Session, joinedload, subqueryload, contains_eager
from sqlalchemy import or_, asc, desc
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, select
from collections import defaultdict
import pprint



class ConversationRepository(IConversationRepository):

    def get_conversation_by_id(self, session: Session, conversation_id: int) -> Conversation:
        message_sub = session.query(Message.message_id).filter(Message.conversation_id == conversation_id).order_by(Message.message_id.desc()).limit(10).subquery()
        result = session.query(Conversation).options(joinedload(Conversation.messages.and_(Message.message_id.in_(message_sub)))).first()
        pprint.pprint(result)
        result.messages.reverse()
        return result

    def get_conversation_by_two_user_id(self, session: Session, first_user_id: int, second_user_id: int) -> Conversation:
        participants_exist = (
            session.query(Participant)
            .filter(Participant.user_id.in_([first_user_id, second_user_id]))
            .first()
        )
        if not participants_exist:
            print('Chua co participant')
            return None

        # subquery = session.query(Participant.conversation_id).group_by(Participant.conversation_id).filter(Participant.user_id.in_([first_user_id, second_user_id])).having(func.count(Participant.user_id) == 2).subquery()
        conversation = session.query(Conversation).filter(Conversation.conversation_id.in_([participants_exist.conversation_id])).first()
        return conversation
    
    def create_conversation(self, session: Session, conversation: Conversation):
            session.add(instance=conversation)
            return conversation
        
    def get_conversations_by_user_id(self, session: Session, user_id: int, limit: int = 10):
        subquery = session.query(Participant.conversation_id).filter(Participant.user_id == user_id).subquery()
        
        
        row_number = func.row_number().over( #đánh số thứ tự rank của từng message ứng với conversation_id
            partition_by=Message.conversation_id,
            order_by=Message.message_id.desc()
        ).label('rn')

        message_sub = session.query(Message, row_number).filter(Message.conversation_id.in_(subquery)).order_by(Message.conversation_id.asc()).cte()

        conversations = []
        conversation_dict = defaultdict(lambda: {"conversation": None, "messages": []})
        results = session.query(Conversation, Message).options(contains_eager(Conversation.messages)).join(message_sub, Conversation.conversation_id == message_sub.c.conversation_id).join(Message, message_sub.c.message_id == Message.message_id).filter(message_sub.c.rn <= limit).order_by(message_sub.c.message_id.desc(), Conversation.lastest_updated.desc()).all() 
        for conv, mess in results:
            if (conversation_dict[conv.conversation_id]['conversation'] is None):
                conv.messages = []
                conversation_dict[conv.conversation_id]['conversation'] = conv
            conversation_dict[conv.conversation_id]['messages'].append(mess)

        for key in conversation_dict.keys():
            conv = conversation_dict[key]['conversation']
            conversation_dict[key]['messages'].reverse()
            conv.messages = conversation_dict[key]['messages']
            conversations.append(conv)
        return conversations

     
    def delete_conversation(self, session: Session, conversation_id):
        pass

    def add_message_to_conversation(self, session: Session, message: Message) -> Message:
            session.add(message)
            return message

    def get_message_from_conversation(self, session: Session, cursor: int, conversation_id: int, limit: int = 10) -> List[Message]:
        results = session.query(Message).filter(Message.conversation_id == conversation_id, Message.message_id < cursor).order_by(Message.message_id.desc()).limit(limit=limit).all()
        results.reverse()
        return results


    # def add_list_members_to_conversation(self, conversation: Conversation, members: List[ConversationMember]):
    #     try:
    #         conversation.members.extend(members)
    #         session.commit()
    #     except SQLAlchemyError as e:
    #         print(e)
    #         session.rollback()