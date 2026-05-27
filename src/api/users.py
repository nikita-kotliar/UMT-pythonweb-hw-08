from fastapi import APIRouter, Depends, UploadFile, File, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserResponse
from src.repository import users as user_repo
from src.services.auth import get_current_user
from src.services.cloudinary_service import upload_avatar

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
async def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch("/me/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contents = await file.read()
    url = upload_avatar(contents, str(current_user.id))
    return user_repo.update_avatar(db, current_user, url)
