from sqlmodel import Field, SQLModel
from typing import List, Union
from pydantic import UUID4
from pydantic.functional_validators import field_validator
from email_validator import validate_email, EmailNotValidError

from backend.app.db.types import DatetimeTypeMixin
from backend.app.db.exceptions import InvalidEmailException


# Shared properties
# TODO: replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel, DatetimeTypeMixin):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Union[str, None] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, email):
        try:
            validate_email(email)
        except EmailNotValidError:
            raise InvalidEmailException()

        return email


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: Union[str, None] = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: Union[str, None] = None  # type: ignore
    password: Union[str, None] = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: Union[str, None] = None
    email: Union[str, None] = None


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int


# Database model, database table inferred from class name
class User(UserBase):
    __tablename__ = "users"

    id: UUID4 = Field(default=None, primary_key=True)
    hashed_password: str


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


class NewPassword(SQLModel):
    token: str
    new_password: str
