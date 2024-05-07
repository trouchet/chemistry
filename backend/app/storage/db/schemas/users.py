from sqlmodel import Field, SQLModel
from pydantic.functional_validators import field_validator
from pydantic import UUID4
from email_validator import validate_email, EmailNotValidError

from datetime import datetime   

from ..base.types import PrimaryKeyType
from app.storage.db import InvalidEmailException

def get_current_timestamp():
    return datetime.now()

class DatetimeTypeMixin:
    created_at: datetime = Field(
        index=True, default=get_current_timestamp
    )
    updated_at: datetime = Field(
        index=True, default=get_current_timestamp
    )

    @field_validator("created_at")
    @classmethod
    def validate_created_at(cls, created_at):
        return created_at

    @field_validator("updated_at")
    @classmethod
    def validate_updated_at(cls, updated_at):
        return updated_at

    @classmethod
    def get_current_timestamp(cls):
        return get_current_timestamp()

    @classmethod
    def get_current_timestamp(cls):
        return get_current_timestamp()

   
# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    signed_up_at: datetime = Field(
        index=True, default=get_current_timestamp
    )
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None

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
    full_name: str | None = None

# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None

class UpdatePassword(SQLModel):
    current_password: str
    new_password: str

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: PrimaryKeyType = Field(UUID4, default=None, primary_key=True)
    hashed_password: str

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str