from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.config import settings
from src.storage.db.schemas import User
from src.storage.db.repositories import UsersRepository
from src.base.exceptions import CredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_user(
    token: str = Depends(oauth2_scheme),
) -> Optional[User]:
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        provider_id: str = payload.get("id")

        if provider_id is None:
            raise CredentialsException()

        token_data = TokenData(id=id)

    except JWTError:
        raise CredentialsException()

    user = await UsersRepository().get_by_id(token_data.id)
    if not user:
        raise CredentialsException()
    else: 
        return user
