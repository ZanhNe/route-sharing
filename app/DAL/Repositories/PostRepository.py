from app.DAL.Interfaces.IPostRepository import IPostRepository
from typing import List
from app.GUI.model.models import Post
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class PostRepository(IPostRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_posts_all(self) -> List[Post]:
        return self.session.query(Post).all()
    
    def get_post(self, post_id: int) -> Post:
        return self.session.query(Post).get(ident=post_id)
    
    def add_post(self, post: Post) -> Post:
        try: 
            self.session.add(post)
            self.session.commit()
            return post 
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None
    
    def update_post(self, post: Post, updated_post: Post) -> Post:
        try:
            post.title = updated_post.title
            post.content = updated_post.content
            post.image_url = updated_post.image_url
            post.type = updated_post.type
            post.updated_date = updated_post.updated_date
            post.status_match = updated_post.status_match
            self.session.commit()
            return post
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return None
    
    def delete_post(self, post: Post) -> bool:
        try:
            self.session.delete(post)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            print(e)
            self.session.rollback()
            return False
    
        