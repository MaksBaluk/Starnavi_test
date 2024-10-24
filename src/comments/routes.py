from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.db import get_db
from .services import CommentService  # Імпортуйте ваш сервіс для коментарів
from .schemas import CommentCreate, Comment, CommentUpdate  # Імпортуйте ваші схеми для коментарів
from auth.authentication import get_current_user
from src.core.base import get_service, BaseService

router = APIRouter(prefix="/api", tags=["comments"])


def get_comment_service(db: Session = Depends(get_db)) -> BaseService:
    return get_service(CommentService, db)


@router.post("/post/{post_id:int}/comment", response_model=Comment)
async def create_new_comment(
        post_id: int,
        comment: CommentCreate,
        service: CommentService = Depends(get_comment_service),
        current_user=Depends(get_current_user)
):
    new_comment = service.create_comment(comment, post_id=post_id, owner_id=current_user.id)

    return new_comment


# Отримати коментар за ID
@router.get("/comment/{comment_id:int}", response_model=Comment)
def get_comment(comment_id: int, service: CommentService = Depends(get_comment_service)):
    return service.get_comment_by_id(comment_id)


# Отримати всі коментарі для певного поста
@router.get('/post/{post_id:int}/comments', response_model=list[Comment])
def get_comments_for_post(post_id: int, service: CommentService = Depends(get_comment_service)):
    return service.get_comments_by_post_id(post_id)


# Оновити коментар
@router.patch("/comment/{comment_id:int}", response_model=Comment)
def update_comment(comment_id: int, comment_update: CommentUpdate,
                   service: CommentService = Depends(get_comment_service),
                   current_user=Depends(get_current_user)):
    comment = service.get_comment_by_id(comment_id)
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    return service.update_comment_crud(comment_id, comment_update)


# Видалити коментар
@router.delete("/comment/{comment_id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, service: CommentService = Depends(get_comment_service),
                   current_user=Depends(get_current_user)):
    comment = service.get_comment_by_id(comment_id)
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    service.delete_comment_crud(comment_id)
