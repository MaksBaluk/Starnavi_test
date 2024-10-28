import threading
from typing import Type, List, Dict
from datetime import date
from sqlalchemy import func, Integer
from fastapi import HTTPException
from .models import Comment
from .schemas import CommentCreate, CommentUpdate
from src.core.base import BaseService
from src.utils.moderation import is_toxic_content
from src.posts.models import Post


class CommentService(BaseService):

    def create_comment(self, comment_data: CommentCreate, post_id: int, owner_id: int) -> Comment:
        if is_toxic_content(comment_data.content):
            raise HTTPException(status_code=400, detail="Comment contains toxic content and cannot be posted.")

        new_comment = Comment(**comment_data.dict(), post_id=post_id, owner_id=owner_id)
        self.create(new_comment)

        post = self.db.query(Post).filter(Post.id == post_id).first()
        if post and post.auto_reply_enabled:
            self.schedule_auto_reply(new_comment.id, "Дякуємо за ваш коментар!", post.auto_reply_delay)

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

    def get_comments_daily_breakdown(self, date_from: date, date_to: date) -> List[Dict[str, int]]:
        results = (
            self.db.query(
                func.date(Comment.created_at).label('date'),
                func.count(Comment.id).label('total_comments'),
                func.sum(func.cast(Comment.blocked, Integer)).label('total_blocked')
            )
            .filter(Comment.created_at >= date_from, Comment.created_at <= date_to)
            .group_by(func.date(Comment.created_at))
            .order_by(func.date(Comment.created_at))
            .all()
        )

        return [{'date': str(date), 'total_comments': total_comments, 'total_blocked': total_blocked} for
                date, total_comments, total_blocked in results]

    def schedule_auto_reply(self, comment_id: int, reply_content: str, delay_seconds: int) -> None:

        def auto_reply():
            comment = self.get_comment_by_id(comment_id)
            new_reply = Comment(content=reply_content, post_id=comment.post_id, owner_id=comment.owner_id)
            self.create(new_reply)

        threading.Timer(delay_seconds, auto_reply).start()
