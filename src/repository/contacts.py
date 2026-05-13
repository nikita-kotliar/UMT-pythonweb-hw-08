from datetime import date
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


def get_contacts(
    db: Session,
    first_name: Optional[str],
    last_name: Optional[str],
    email: Optional[str],
) -> list[Contact]:
    query = db.query(Contact)
    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        filters.append(Contact.email.ilike(f"%{email}%"))
    if filters:
        query = query.filter(or_(*filters))
    return query.order_by(Contact.last_name, Contact.first_name).all()


def get_contact(db: Session, contact_id: int) -> Contact | None:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contact_by_email(db: Session, email: str) -> Contact | None:
    return db.query(Contact).filter(Contact.email == email).first()


def create_contact(db: Session, body: ContactCreate) -> Contact:
    contact = Contact(**body.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(db: Session, contact: Contact, body: ContactUpdate) -> Contact:
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact: Contact) -> None:
    db.delete(contact)
    db.commit()


def get_upcoming_birthdays(db: Session) -> list[Contact]:
    today = date.today()
    contacts = db.query(Contact).all()
    result = []
    for contact in contacts:
        try:
            next_birthday = contact.birthday.replace(year=today.year)
        except ValueError:
            next_birthday = contact.birthday.replace(year=today.year, day=28)
        if next_birthday < today:
            try:
                next_birthday = contact.birthday.replace(year=today.year + 1)
            except ValueError:
                next_birthday = contact.birthday.replace(year=today.year + 1, day=28)
        if 0 <= (next_birthday - today).days <= 7:
            result.append(contact)
    return result
