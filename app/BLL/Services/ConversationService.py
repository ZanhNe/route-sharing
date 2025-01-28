from app.GUI.model.models import Conversation, Message, Participant
from typing import List
from app.BLL.Interfaces.IConversationService import IConversationService
from app.DAL.Interfaces.IConversationRepository import IConversationRepository
from app.utils.utils import Helper
from datetime import datetime
class ConversationService(IConversationService):
    def __init__(self, conversation_repo: IConversationRepository):
        self.conversation_repo = conversation_repo

    def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        return self.conversation_repo.get_conversation_by_id(conversation_id=conversation_id)

    def get_conversation_by_two_user_id(self, first_user_id: str, second_user_id: str) -> Conversation:
        return self.conversation_repo.get_conversation_by_two_user_id(first_user_id=first_user_id, second_user_id=second_user_id)
    
    def create_conversation(self, conversation):
        return self.conversation_repo.create_conversation(conversation=conversation)
    
    def delete_conversation(self, conversation_id):
        pass

    def get_conversations_by_user_id(self, user_id) -> List[Conversation]:
        return self.conversation_repo.get_conversations_by_user_id(user_id=user_id)
    
    def get_message_from_conversation(self, cursor: int, conversation_id: int, limit: int = 10) -> List[Message]:
        return self.conversation_repo.get_message_from_conversation(cursor=cursor, conversation_id=conversation_id, limit=limit)

    def handle_private_conversation(self, first_user_id: str, second_user_id: str) -> Conversation:
        try:
            conversation = self.get_conversation_by_two_user_id(first_user_id=first_user_id, second_user_id=second_user_id)
            if (not conversation):
                conversation = Conversation()
                first_participant = Participant(user_id=first_user_id)
                second_participant = Participant(user_id=second_user_id)
                conversation.participants.extend([first_participant, second_participant])

                conversation_after_create = self.create_conversation(conversation=conversation)
                return conversation_after_create
            return conversation
        except Exception as e:
            print(e)
            return None
        
    def add_message_to_conversation(self, conversation: Conversation, sender_id: str, content: str) -> Message:
        message = Message(content=content, sender_id=sender_id, conversation_id=conversation.conversation_id)
        conversation.lastest_updated = datetime.now()
        return self.conversation_repo.add_message_to_conversation(message=message)
            
    # def get_conversation_from_two_user(self, first_user_id: int, second_user_id: int) -> Conversation:
    #     conversation_id = Helper.generate_hash_md5(Helper.sorted_combine_id_to_str(first_user_id, second_user_id))
    #     conversation = self.conversation_repo.get_conversation_by_id(conversation_id=conversation_id)

    #     if (not conversation):
    #         conversation = Conversation(conversation_id=conversation_id)
    #         conversation_after_create = self.conversation_repo.create_conversation(conversation=conversation)
    #         if (not conversation_after_create):
    #             return None
    #         first_cv_mem = ConversationMember(conversation_id=conversation_id, user_id=first_user_id)
    #         second_cv_mem = ConversationMember(conversation_id=conversation_id, user_id=second_user_id)

    #         self.conversation_repo.add_list_members_to_conversation(conversation=conversation_after_create, members=[first_cv_mem, second_cv_mem])
            
    #         return conversation_after_create
    #     return conversation
        