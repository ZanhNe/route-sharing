from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Conversation, User, Message

class IConversationRepository(ABC):

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: int) -> Conversation:
        pass

    @abstractmethod
    def get_conversation_by_two_user_id(self, first_user_id: str, second_user_id: str) -> Conversation:
        pass

    @abstractmethod
    def get_conversations_by_user_id(self, user_id: str) -> List[Conversation]:
        pass
    @abstractmethod
    def get_message_from_conversation(self, cursor: int, conversation_id: int, limit: int = 10) -> List[Message]:
        pass
    @abstractmethod
    def create_conversation(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: int) -> None:
        pass

    @abstractmethod
    def add_message_to_conversation(self, message: Message) -> Message:
        pass


    # @abstractmethod
    # def add_list_members_to_conversation(self, conversation: Conversation, ):
    #     pass

