from fastapi import HTTPException, Depends
from uuid import uuid4
from typing_extensions import Annotated

from ..constants import (
    USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH
)

from ... import logger
from ..utils.security import (
    get_password_hash, 
    create_access_token, 
    is_password_strong
)
from ...db import User
from ..models import UserRequest

from ..exceptions import (
    WeakPasswordException, 
    UserAlreadyExistsException,
    InvalidUsernameException,
    UserRegistrationException
)

from typing import Any

from sqlmodel import Session, select

from ..utils.security import (
    get_password_hash, 
    verify_password
)
from ...db.models.users import (
    User, 
    UserCreate, 
    UserUpdate
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
