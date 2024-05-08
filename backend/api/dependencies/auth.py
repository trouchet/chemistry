from fastapi import Depends

from typing_extensions import Annotated

from .users import CurrentUserDependency
from backend.storage.db.schemas import User

async def validate_is_authenticated(
    current_user: CurrentUserDependency,
) -> User:
    """
    This just returns as the CurrentUserDep dependency already throws if there is an issue with the auth token.
    """
    return current_user

AuthenticationDependency = Annotated[User, Depends(validate_is_authenticated)]
