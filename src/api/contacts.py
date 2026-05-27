from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.services import contacts as service
from src.services.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    body: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_contact(db, body, current_user)


@router.get("/", response_model=list[ContactResponse])
def get_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_contacts(db, current_user, first_name, last_name, email)


@router.get("/birthdays", response_model=list[ContactResponse])
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_upcoming_birthdays(db, current_user)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_contact(db, contact_id, current_user)


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    body: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.update_contact(db, contact_id, body, current_user)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service.delete_contact(db, contact_id, current_user)
