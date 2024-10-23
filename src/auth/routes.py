from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .authentication import create_access_token, get_current_user, create_refresh_token
from .schemas import UserCreate, Token, User, Login, UserProfile
from .services import UserService
from .utils import verify_password
from db import get_db
from config import settings
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)

    existing_user = user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    try:
        user = user_service.create_user(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user: " + str(e)
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login(form_data: Login = Depends(), db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_email(form_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user = UserService(db).get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
def get_user(current_user=Depends(get_current_user)):
    return current_user


@router.get('/profile/{user_id:int}', response_model=UserProfile, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService(db).get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
