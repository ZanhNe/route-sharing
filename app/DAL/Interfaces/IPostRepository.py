from abc import ABC, abstractmethod
from typing import List
from app.GUI.model.models import Post

class IPostRepository(ABC):
    @abstractmethod
    def get_posts_all(self) -> List[Post]:
        pass

    @abstractmethod
    def get_post(self, post_id: int) -> Post:
        pass
    
    @abstractmethod
    def add_post(self, post: Post) -> Post:
        pass

    @abstractmethod
    def update_post(self, post: Post, updated_post: Post) -> Post:
        pass

    @abstractmethod
    def delete_post(self, post: Post) -> bool:
        pass