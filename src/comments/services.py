from typing import Type

from .models import Comment
from .schemas import CommentCreate, CommentUpdate
from src.core.base import BaseService


class CommentService(BaseService):

    def create_comment(self, comment_data: CommentCreate, post_id: int, owner_id: int) -> Comment:
        new_comment = Comment(**comment_data.dict(), post_id=post_id, owner_id=owner_id)
        self.create(new_comment)
        return new_comment

    def get_comment_by_id(self, comment_id: int) -> Comment:
        return self.get_or_404(Comment, comment_id)

    def get_comments_by_post_id(self, post_id: int) -> list[Type[Comment]]:
        return self.db.query(Comment).filter(Comment.post_id == post_id).all()

    def get_all_comments_crud(self) -> list[Type[Comment]]:
        return self.db.query(Comment).all()

    def update_comment_crud(self, comment_id: int, data: CommentUpdate) -> Comment:
        post = self.get_or_404(Comment, comment_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(post, key, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_comment_crud(self, comment_id: int) -> None:
        post = self.get_comment_by_id(comment_id)
        self.delete(post)
