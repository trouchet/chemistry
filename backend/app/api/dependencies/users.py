from fastapi import Depends
from typing_extensions import Annotated
from jwt import PyJWTError, decode
from pydantic import ValidationError

from ... import settings

from ...models.users import User

from ..exceptions import (
    CredentialsException,
    UserNotFoundException,
    InactiveUserException,
    InsufficientPrivilegesException,
)

from .auth import TokenDependency
from .session import DatabaseSessionDependency

from ...models.token import TokenPayload


def get_current_user(
    session: DatabaseSessionDependency, token: TokenDependency
) -> User:
    try:
        secret = settings.SECRET_KEY
        algorithms = [settings.JWT_ALGORITHM]
        payload = decode(token, secret, algorithms=algorithms)

        token_data = TokenPayload(**payload)

    except (PyJWTError, ValidationError):
        raise CredentialsException()

    user = session.get(User, token_data.sub)

    if not user:
        raise UserNotFoundException()

    if not user.is_active:
        raise InactiveUserException()

    return user


# Dependency to get the current user
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUserDependency) -> User:
    if not current_user.is_superuser:
        raise InsufficientPrivilegesException()

    return current_user


# Dependency to get the current superuser
SuperUserDependency = Depends(get_current_active_superuser)
