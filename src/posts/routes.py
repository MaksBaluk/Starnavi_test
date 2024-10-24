from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from .services import PostService
from .schemas import PostCreate, Post, PostUpdate, PostOne
from auth.authentication import get_current_user
from src.core.base import get_service, BaseService

router = APIRouter(prefix="/api", tags=["posts"])


def get_post_service(db: Session = Depends(get_db)) -> BaseService:
    return get_service(PostService, db)


@router.post("/post", response_model=Post)
async def create_new_post(post: PostCreate, service: PostService = Depends(get_post_service),
                          current_user=Depends(get_current_user)):
    new_post = service.create_post(post, owner_id=current_user.id)
    return new_post


@router.get("/post/{post_id:int}", response_model=PostOne)
def get_post(post_id: int, service: PostService = Depends(get_post_service)):
    return service.get_post_by_id(post_id)


@router.get('/post', response_model=list[Post])
def get_all_posts(service: PostService = Depends(get_post_service)):
    return service.get_all_posts_crud()


@router.patch("/post/{post_id:int}", response_model=Post)
def update_post(post_id: int, post_update: PostUpdate,
                service: PostService = Depends(get_post_service),
                current_user=Depends(get_current_user)):
    post = service.get_post_by_id(post_id)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return service.update_post_crud(post_id, post_update)


@router.delete("/post/{post_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, service: PostService = Depends(get_post_service),
                current_user=Depends(get_current_user)):
    post = service.get_post_by_id(post_id)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    service.delete_post_crud(post_id)
