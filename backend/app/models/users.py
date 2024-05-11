from sqlmodel import Field, SQLModel
from typing import List, Union
from pydantic import UUID4


# Shared properties
# TODO: replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Union[str, None] = None


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
    id: UUID4 = Field(default=None, primary_key=True)


class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: UUID4 = Field(default=None, primary_key=True)
    hashed_password: str


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


class NewPassword(SQLModel):
    token: str
    new_password: str
