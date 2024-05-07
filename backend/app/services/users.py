from fastapi import HTTPException
from uuid import uuid4

from app import (
    USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH
)

from app import logger
from app.utils.security import hash_password, create_access_token
from app.storage.db import User
from app.dependencies import UserServiceDependency
from app.models import UserRequest
from app.storage.db.dependencies import UserRepositoryDependency
from app.exceptions import (
    WeakPasswordException, 
    UserAlreadyExistsException,
    InvalidUsernameException,
    UserRegistrationException
)
from app.utils.security import is_password_strong

class UserService:
    def __init__(
        self, 
        user_repository: UserRepositoryDependency
    ) -> None:
        self.user_repository = user_repository

    async def _validate_username(self, username: str):
        user_exists = await self.user_repository.filter_by_field("username", username)
        
        if user_exists:
            raise UserAlreadyExistsException(username)

        if len(username) < USERNAME_MIN_LENGTH and \
            len(username) > USERNAME_MAX_LENGTH:
            raise InvalidUsernameException(username)

    async def _validate_password(self, password: str):
        if not is_password_strong(password):
            raise WeakPasswordException(password)

    async def _validate_user_request(self, user_request: UserRequest):
        # Relevant data
        username = user_request["username"]
        password = user_request["password"]

        # Data validation
        # Username validation
        try:
            await self._validate_username(username)
        except Exception as e:
            raise UserRegistrationException()
        
        # Password validation
        try:
            await self._validate_password(password)
        except Exception as e:
            raise UserRegistrationException()

    async def register(
        self, 
        user_request: UserRequest,
        user_repository: UserServiceDependency
    ) -> UserRequest:
        # Validate the user request
        try:
            await self._validate_user_request(user_request)
        except HTTPException as e:
            raise UserRegistrationException()

        # Create an access token
        user_request = user_request.dict()
        access_token = create_access_token(user_request)
        
        # Hash the password using a secure algorithm
        hashed_password = hash_password(user_request["password"])

        # Create a new provider instance with the hashed password
        user = User(
            id=uuid4(),
            username=user_request["username"],
            hashed_password=hashed_password,
            token_str=access_token,
        )

        # Database Persistence with Transaction Handling
        try:
            await user_repository.save(user)
        
        except Exception as e:
            await user_repository.session.rollback()
            logger.error(f"Failed to save provider to database: {e}")
            raise 
        
        return UserRequest(**user.dict(exclude={"hashed_password"}))

