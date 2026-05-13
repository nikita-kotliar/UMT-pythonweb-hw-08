from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    birthday: date
    additional_data: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, min_length=7, max_length=20)
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class ContactResponse(ContactBase):
    id: int

    model_config = {"from_attributes": True}
