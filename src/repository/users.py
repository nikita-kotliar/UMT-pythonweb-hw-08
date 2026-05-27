from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserCreate
from src.services.auth import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, body: UserCreate) -> User:
    user = User(
        username=body.username,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_email(db: Session, user: User) -> User:
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user


def update_avatar(db: Session, user: User, url: str) -> User:
    user.avatar = url
    db.commit()
    db.refresh(user)
    return user


def update_refresh_token(db: Session, user: User, token: str | None) -> None:
    user.refresh_token = token
    db.commit()
