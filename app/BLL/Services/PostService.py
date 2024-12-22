from app.BLL.Interfaces.IPostService import IPostService
from app.DAL.Interfaces.IPostRepository import IPostRepository
from typing import List
from app.GUI.model.models import Post

class PostService(IPostService):
    def __init__(self, post_repository: IPostRepository) -> None:
        self.post_repository = post_repository

    def get_posts_all(self) -> List[Post]:
        return self.post_repository.get_posts_all(), 200
    
    def get_post(self, post_id: int) -> Post:
        post = self.post_repository.get_post(post_id=post_id)
        if (not post):
            return {'error': 'Không tồn tại Post'}, 404
        return post, 200
    
    def add_post(self, post: Post) -> Post:
        post = self.post_repository.add_post(post=post)
        if (not post):
            return {'error': 'Lỗi khi thêm Post mới'}, 400
        return post, 200
    
    def update_post(self, post: Post, updated_post: Post) -> Post:
        new_post = self.post_repository.update_post(post=post, updated_post=updated_post)
        if (not new_post):
            return {'error': 'Lỗi khi cập nhật Post hiện tại'}, 400
        return new_post, 200
    
    def delete_post(self, post: Post) -> bool:
        flag = self.post_repository.delete_post(post=post)
        if (not flag):
            return {'error': 'Lỗi khi xóa Post hiện tại'}, 400
        return flag, 200