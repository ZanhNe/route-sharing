from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Conversation, Message

class IConversationService(ABC):



    @abstractmethod
    def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        pass

    @abstractmethod
    def get_conversation_by_two_user_id(self, first_user_id: int, second_user_id: int) -> Conversation:
        pass

    @abstractmethod
    def create_conversation(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: str) -> None:
        pass
        
    @abstractmethod
    def handle_private_conversation(self, first_user_id: int, second_user_id: int) -> Conversation:
        pass

    @abstractmethod
    def add_message_to_conversation(self, conversation_id: int, sender_id: int, content: str) -> Message:
        pass
    # @abstractmethod
    # def get_conversation_from_two_user(self, first_user_id: int, second_user_id: int) -> Conversation:
    #     pass