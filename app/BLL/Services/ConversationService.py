from app.GUI.model.models import Conversation, Message, Participant
from typing import List
from app.BLL.Interfaces.IConversationService import IConversationService
from app.DAL.Interfaces.IConversationRepository import IConversationRepository
from app.utils.utils import Helper
from app.custom.Helper.Helper import TransactionManager
from datetime import datetime
from injector import inject

class ConversationService(IConversationService):
    @inject
    def __init__(self, conversation_repo: IConversationRepository, tm: TransactionManager):
        self.conversation_repo = conversation_repo
        self.tm = tm

    def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        with self.tm.transaction('') as session:
            return self.conversation_repo.get_conversation_by_id(session=session, conversation_id=conversation_id)

    def get_conversation_by_two_user_id(self, first_user_id: str, second_user_id: str) -> Conversation:
        with self.tm.transaction('') as session:    
            return self.conversation_repo.get_conversation_by_two_user_id(session=session, first_user_id=first_user_id, second_user_id=second_user_id)
    
    def create_conversation(self, conversation):
        with self.tm.transaction('Lỗi khi tạo conversation') as session:
            return self.conversation_repo.create_conversation(session=session, conversation=conversation)
    
    def delete_conversation(self, conversation_id):
        pass

    def get_conversations_by_user_id(self, user_id) -> List[Conversation]:
        with self.tm.transaction('') as session:
            return self.conversation_repo.get_conversations_by_user_id(session=session, user_id=user_id)
    
    def get_message_from_conversation(self, cursor: int, conversation_id: int, limit: int = 10) -> List[Message]:
        with self.tm.transaction('') as session:    
            return self.conversation_repo.get_message_from_conversation(session=session, cursor=cursor, conversation_id=conversation_id, limit=limit)

    def handle_private_conversation(self, first_user_id: str, second_user_id: str) -> Conversation:
        with self.tm.transaction('Lỗi khi xử lý private con') as session:
            conversation = self.get_conversation_by_two_user_id(first_user_id=first_user_id, second_user_id=second_user_id)
            if (not conversation):
                conversation = Conversation()
                first_participant = Participant(user_id=first_user_id)
                second_participant = Participant(user_id=second_user_id)
                conversation.participants.extend([first_participant, second_participant])

                conversation_after_create = self.create_conversation(conversation=conversation)
                return conversation_after_create
            return conversation
        
    def add_message_to_conversation(self, conversation: Conversation, sender_id: str, content: str) -> Message:
        with self.tm.transaction('Lỗi khi xử lý private con') as session:
            message = Message(content=content, sender_id=sender_id, conversation_id=conversation.conversation_id)
            conversation.lastest_updated = datetime.now()

            for participant in conversation.participants:
                if participant.user_id == sender_id:
                    participant.last_viewed = datetime.now()

            return self.conversation_repo.add_message_to_conversation(session=session, message=message)
    
    def update_last_viewed_participant(self, user_id: str, conversation_id: int):
        with self.tm.transaction('') as session:
            conversation = self.conversation_repo.get_conversation_by_id(session=session, conversation_id=conversation_id)
            for participant in conversation.participants:
                if participant.user_id == user_id:
                    participant.last_viewed = datetime.now()
        return True
    
        