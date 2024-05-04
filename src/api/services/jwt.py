from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..models import Provider, TokenData

from core.config import settings
from src.db.repositories import providers_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_current_provider(
    token: str = Depends(oauth2_scheme),
) -> Optional[Provider]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        provider_id: str = payload.get("provider_id")

        if provider_id is None:
            raise credentials_exception

        token_data = TokenData(provider_id=provider_id)

    except JWTError:
        raise credentials_exception

    provider = await providers_repository.get_by_id(token_data.provider_id)
    if provider is None:
        raise credentials_exception

    return provider
