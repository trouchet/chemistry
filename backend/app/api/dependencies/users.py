from typing import Annotated, Optional 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode
from pydantic import ValidationError

from backend.app import logger, settings

from backend.app.db.models import User

from ..exceptions import (
    CredentialsException, 
    UserNotFoundException,
    InactiveUserException
)

from .auth import TokenDependency
from .session import DatabaseSessionDependency

from backend.app.db.models.token import TokenPayload

def get_current_user(
    session: DatabaseSessionDependency, 
    token: TokenDependency
) -> User:
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise CredentialsException()
    user = session.get(User, token_data.sub)
    
    if not user:
        raise UserNotFoundException()
    
    if not user.is_active:
        raise InactiveUserException()
    
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUserDependency) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user