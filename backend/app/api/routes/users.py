from typing import Any

from fastapi import APIRouter
from sqlmodel import func, select
from pydantic import UUID4

from backend.app.exceptions import (
    InexistentUserException,
    SuperUserForbiddenException,
    UserAlreadyExistsByEMailException,
    WrongPasswordException,
    SamePreviousPasswordException,
    OpenRegistrationForbiddenException,
    InsufficientPrivilegesException,
    InexistentUserByIDException,
)

from ..dependencies.session import DatabaseSessionDependency
from ..dependencies.users import (
    CurrentUserDependency,
    SuperUserDependency,
)

from ..services.users import get_user_by_email

from ..utils.security import get_password_hash, verify_password
from ..utils.email import generate_new_account_email, send_email
from backend.app import settings
from ..services.users import create_user, update_user

from ...models.users import (
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from ...models.email import Message

router = APIRouter()


@router.get(
    "/",
    dependencies=[SuperUserDependency],
    response_model=UsersPublic,
)
def read_users(
    session: DatabaseSessionDependency, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve users.
    """

    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.post("/", dependencies=[SuperUserDependency], response_model=UserPublic)
def create_user_(*, session: DatabaseSessionDependency, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise UserAlreadyExistsByEMailException()

    user = create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )

        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return user


@router.patch("/me", response_model=UserPublic)
def update_user_me(
    *,
    session: DatabaseSessionDependency,
    user_in: UserUpdateMe,
    current_user: CurrentUserDependency,
) -> Any:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user:
            if existing_user.id != current_user.id:
                raise UserAlreadyExistsByEMailException()

    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *,
    session: DatabaseSessionDependency,
    body: UpdatePassword,
    current_user: CurrentUserDependency,
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise WrongPasswordException()

    if body.current_password == body.new_password:
        raise SamePreviousPasswordException()

    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()

    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUserDependency) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
def delete_user_me(
    session: DatabaseSessionDependency, current_user: CurrentUserDependency
) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise SuperUserForbiddenException()

    session.delete(current_user)
    session.commit()

    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
def register_user(session: DatabaseSessionDependency, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise OpenRegistrationForbiddenException()

    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise UserAlreadyExistsByEMailException()

    user_create = UserCreate.model_validate(user_in)

    user = create_user(session=session, user_create=user_create)
    return user


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: UUID4,
    session: DatabaseSessionDependency,
    current_user: CurrentUserDependency,
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)

    if user == current_user:
        return user

    if not current_user.is_superuser:
        raise InsufficientPrivilegesException()

    return user


@router.patch(
    "/{user_id}",
    dependencies=[SuperUserDependency],
    response_model=UserPublic,
)
def update_user_(
    *,
    session: DatabaseSessionDependency,
    user_id: UUID4,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = session.get(User, user_id)
    if not db_user:
        raise InexistentUserByIDException()

    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise UserAlreadyExistsByEMailException()

    db_user = update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[SuperUserDependency], response_model=Message)
def delete_user(
    session: DatabaseSessionDependency,
    current_user: CurrentUserDependency,
    user_id: UUID4,
) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise InexistentUserException()

    if user == current_user:
        raise SuperUserForbiddenException()

    session.delete(user)
    session.commit()

    return Message(message="User deleted successfully")
