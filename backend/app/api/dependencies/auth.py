from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing_extensions import Annotated

from ... import settings

# OAuth2PasswordBearer instance
tokenUrl = f"{settings.API_V1_STR}/login/access-token"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=tokenUrl)

# Dependency to get token
TokenDependency = Annotated[str, Depends(reusable_oauth2)]

# Dependency to get password form
PasswordFormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]
