from typing import Annotated, Optional 
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import JWTError

from src.storage.db.schemas import User
from src.storage.db.repositories import UsersRepository
from src.exceptions import CredentialsException
from src.utils.security import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
TokenDependency = Annotated[str, Depends(oauth2_scheme)]

async def get_current_user(
    token: TokenDependency,
) -> Optional[User]:
    try:
        payload = decode_jwt(token)
        username_candidate: str = payload.get("sub")

        if not username_candidate:
            raise CredentialsException()
        
        permissions = payload.get("permissions")
        if permissions is None:
            raise CredentialsException()

    except JWTError:
        raise CredentialsException()

    user = await UsersRepository().get_by_username(username_candidate)
    if not user:
        raise CredentialsException()
    else: 
        return user

CurrentUserDependency = Annotated[User, Depends(get_current_user)]