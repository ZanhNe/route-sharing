from app.GUI.model.models import Conversation, Message
from typing import List
from app.BLL.Interfaces.IConversationService import IConversationService
from app.DAL.Interfaces.IConversationRepository import IConversationRepository
from app.utils.utils import Helper

class ConversationService(IConversationService):
    def __init__(self, conversation_repo: IConversationRepository):
        self.conversation_repo = conversation_repo

    def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        return self.conversation_repo.get_conversation_by_id(conversation_id=conversation_id)

    def get_conversation_by_two_user_id(self, first_user_id: int, second_user_id: int) -> Conversation:
        return self.conversation_repo.get_conversation_by_two_user_id(first_user_id=first_user_id, second_user_id=second_user_id)
    
    def create_conversation(self, conversation):
        return self.conversation_repo.create_conversation(conversation=conversation)
    
    def delete_conversation(self, conversation_id):
        pass

    def handle_private_conversation(self, first_user_id: int, second_user_id: int) -> Conversation:
        try:
            conversation = self.get_conversation_by_two_user_id(first_user_id=min(first_user_id, second_user_id), second_user_id=max(first_user_id, second_user_id))
            if (not conversation):
                conversation = Conversation(main_user_id=first_user_id, secondary_user_id=second_user_id)
                conversation_after_create = self.create_conversation(conversation=conversation)
                return conversation_after_create
            return conversation
        except Exception as e:
            print(e)
            return None
        
    def add_message_to_conversation(self, conversation_id: int, sender_id: int, content: str) -> Message:
        message = Message(content=content, sender_id=sender_id, conversation_id=conversation_id)
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
        