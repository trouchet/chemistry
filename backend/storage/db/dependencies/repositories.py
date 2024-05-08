from typing_extensions import Annotated

from fastapi import Depends

from ..repositories import UserRepository

def get_user_repository(): 
    return UserRepository()

UserRepositoryDependency = Annotated[
    UserRepository, Depends(get_user_repository)
]

