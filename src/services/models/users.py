from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.utils.security import hash_password, create_access_token
from src.db.repositories import UsersRepository
from src.db.schemas import User
from src.models import UserRequest
from src.base.exceptions import WeakPasswordException
from src.constants import USERNAME_MIN_LENGTH
from src.utils.security import is_password_strong
from src.setup.logging import logger

# Username requirements
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

async def vaildate_username_and_password(
    user_repository: UsersRepository,
    username: str, 
    password: str, 
    session: AsyncSession
):
    user_exists = await user_repository.filter_by_field(
        "username", username, session
    )
    
    if existing_provider:
        err_msg = "This username is already taken."
        raise HTTPException(status_code=400, detail=err_msg)

    has_bounded_length = len(username) < USERNAME_MIN_LENGTH and \
                         len(username) > USERNAME_MAX_LENGTH 

    if has_bounded_length:
        msg = f"The username needs to be at least {USERNAME_MIN_LENGTH} characters."
        raise HTTPException(status_code=400, detail=msg)

    if not is_password_strong(password):
        raise WeakPasswordException(password)

class UserService:
    async def register(
        self, 
        provider_data: dict
    ) -> UserRequest:
        # Relevant data
        username = provider_data["username"]
        password = provider_data["password"]

        user_repository = UsersRepository()

        # Data validation
        try:
            await vaildate_username_and_password(username, password)
        except Exception as e:
            logger.error(f"Error during provider registration validation: {e}")
            raise HTTPException(status_code=500, detail="Internal server error during registration.")

        access_token = create_access_token(
            {"username": username, "password": password}
        )

        # Hash the password using a secure algorithm (e.g., bcrypt)
        hashed_password = hash_password(password)

        # Create a new provider instance with the hashed password
        provider = User(
            id=uuid4(),
            username=username,
            hashed_password=hashed_password,
            token_str=access_token,
        )

        # Database Persistence with Transaction Handling (assuming supported by your ORM)
        async with session.begin():
            try:
                await user_repository.save(provider, session)
                # Additional operations within the transaction (if needed)
            except Exception as e:
                await session.rollback()
                logger.error(f"Failed to save provider to database: {e}")
                raise HTTPException(status_code=500, detail="Failed to register provider.")
        
        return UserRequest(**provider.dict(exclude={"hashed_password"}))

