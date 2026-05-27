from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserCreate, UserResponse, TokenResponse
from src.repository import users as user_repo
from src.services.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_email_from_token,
    get_current_user,
)
from src.services.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if user_repo.get_user_by_email(db, body.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    if user_repo.get_user_by_username(db, body.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")

    user = user_repo.create_user(db, body)
    background_tasks.add_task(send_verification_email, user.email, user.username)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_repo.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    user_repo.update_refresh_token(db, user, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    email = get_email_from_token(token)
    user = user_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.is_verified:
        return {"message": "Email already verified"}
    user_repo.verify_email(db, user)
    return {"message": "Email verified successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    request: Request,
    db: Session = Depends(get_db),
):
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    from jose import JWTError, jwt
    from src.conf.config import settings

    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("scope") != "refresh_token":
            raise credentials_exc
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exc

    user = user_repo.get_user_by_email(db, email)
    if not user or user.refresh_token != token:
        raise credentials_exc

    access_token = create_access_token({"sub": email})
    refresh_token = create_refresh_token({"sub": email})
    user_repo.update_refresh_token(db, user, refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token}
