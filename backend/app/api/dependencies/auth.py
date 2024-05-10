from fastapi import Depends
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm
)


from typing_extensions import Annotated
from sqlmodel import Session


from .users import CurrentUserDependency
from ...db.models import User
from ... import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/login/access-token"
)

TokenDependency = Annotated[str, Depends(reusable_oauth2)]

PasswordFormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]