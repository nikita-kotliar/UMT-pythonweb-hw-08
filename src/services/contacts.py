from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate
from src.repository import contacts as repository


def get_contacts(
    db: Session,
    first_name: Optional[str],
    last_name: Optional[str],
    email: Optional[str],
) -> list[Contact]:
    return repository.get_contacts(db, first_name, last_name, email)


def get_contact(db: Session, contact_id: int) -> Contact:
    contact = repository.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


def create_contact(db: Session, body: ContactCreate) -> Contact:
    if repository.get_contact_by_email(db, body.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return repository.create_contact(db, body)


def update_contact(db: Session, contact_id: int, body: ContactUpdate) -> Contact:
    contact = repository.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if body.email and body.email != contact.email:
        if repository.get_contact_by_email(db, body.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return repository.update_contact(db, contact, body)


def delete_contact(db: Session, contact_id: int) -> None:
    contact = repository.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    repository.delete_contact(db, contact)


def get_upcoming_birthdays(db: Session) -> list[Contact]:
    return repository.get_upcoming_birthdays(db)
