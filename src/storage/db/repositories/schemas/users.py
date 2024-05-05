from typing import TypeVar
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.db.base.types import Base
from src.storage.db.schemas import (
    User,
)

from .repository import SQLRepository

# Username requirements
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)

# Repositórios
class UsersRepository(SQLRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> User:
        try:
            return self.find_by_field(field="username", value=username)
        except Exception as e:
            action = f'get user by username {username}'
            await self.__raise_repository_exception(action, e)

    async def vaildate_username(
        self, username: str, password: str
    ):
        user_exists = await self.filter_by_field("username", username)
        
        if user_exists:
            err_msg = "This username is already taken."
            raise HTTPException(status_code=400, detail=err_msg)

        has_bounded_length = len(username) < USERNAME_MIN_LENGTH and \
                            len(username) > USERNAME_MAX_LENGTH 

        if has_bounded_length:
            msg = f"The username needs to be at least {USERNAME_MIN_LENGTH} characters."
            raise HTTPException(status_code=400, detail=msg)

        if not is_password_strong(password):
            raise WeakPasswordException(password)