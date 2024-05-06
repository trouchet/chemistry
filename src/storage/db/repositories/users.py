from typing_extensions import Annotated

from fastapi import Depends

from src.storage.db.dependencies import DatabaseSessionDependency

from src.storage.db import (
    Base,
    User,
)

from .base import SQLRepository

# Repositórios
class UsersRepository(SQLRepository):
    def __init__(self, session: DatabaseSessionDependency) -> None:
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> User:
        try:
            return self.find_by_field(field="username", value=username)
        except Exception as e:
            action = f'get user by username {username}'
            await self.__raise_repository_exception(action, e)


def get_users_repository(): 
    return UsersRepository()

UserRepositoryDependency = Annotated[
    UsersRepository, Depends(get_users_repository)
]
