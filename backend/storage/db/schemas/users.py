from sqlmodel import Field, SQLModel
from pydantic.functional_validators import field_validator
from pydantic import UUID4
from email_validator import validate_email, EmailNotValidError

from datetime import datetime   

from backend.storage.db.base.types import DatetimeTypeMixin
from backend.storage.db.exceptions import InvalidEmailException

# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel, DatetimeTypeMixin):
    email: str = Field(unique=True, index=True)
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
    id: UUID4 = Field(default=None, primary_key=True)
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