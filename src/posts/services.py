from typing import Type
from fastapi import HTTPException
from utils.moderation import is_toxic_content
from .models import Post
from .schemas import PostCreate, PostUpdate
from src.core.base import BaseService


class PostService(BaseService):

    def create_post(self, post_data: PostCreate, owner_id: int) -> Post:
        if is_toxic_content(post_data.content):
            raise HTTPException(status_code=400, detail="Post contains toxic content and cannot be created.")

        new_post = Post(**post_data.dict(), owner_id=owner_id)
        self.create(new_post)
        return new_post

    def get_post_by_id(self, post_id: int) -> Post:
        return self.get_or_404(Post, post_id)

    def get_all_posts_crud(self) -> list[Type[Post]]:
        return self.db.query(Post).all()

    def update_post_crud(self, post_id: int, data: PostUpdate) -> Post:
        post = self.get_or_404(Post, post_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(post, key, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete_post_crud(self, post_id: int) -> None:
        post = self.get_post_by_id(post_id)
        self.delete(post)
