from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from fastapi import Depends
 
from src.core.security import (
    hash_password, 
    create_access_token
)
from src.database.session import get_db_session
from src.database.repositories import providers_repository
from src.database.schemas import Provider
from src.api.models import (
    ProviderRequestModel, 
    WeakPasswordException
)
from src.api.constants import USERNAME_MIN_LENGTH
from src.api.utils.security import is_password_strong
from src.api.setup.logging import logger

class ProviderService:
    async def register(
        self,
        provider_data: dict, 
        session: AsyncSession
    ) -> ProviderRequestModel:
        # Relevant data
        username = provider_data["username"]
        password = provider_data["password"]
        
        # Data validation
        filters = {
            'prov_username':  username
        }
        provider_exists = await providers_repository.find_by_filters(filters, session)

        if provider_exists:
            err_msg = "This provider username is already taken."
            raise HTTPException(status_code=400, detail=err_msg)

        if len(username) < USERNAME_MIN_LENGTH:
            msg = f"The provider username needs to be at least {USERNAME_MIN_LENGTH} characters."
            raise HTTPException(status_code=400, detail=msg)

        if not is_password_strong(password):
            raise WeakPasswordException(password)
        
        data = {
            "prov_username": username,
            "prov_password": password
        }
        access_token = create_access_token(data)

        # Hash the password using a secure algorithm (e.g., bcrypt)
        hashed_password = hash_password(password)

        # Create a new provider instance with the hashed password
        provider = Provider(
            prov_id = uuid4(),
            prov_username = username,
            prov_hashed_password = hashed_password,
            prov_token_str = access_token,
        )
        
        try:
            await providers_repository.save(provider, session)
        except Exception as e:
            logger.error(f"Failed to save provider to database: {e}")
            raise HTTPException(status_code=500, detail="Failed to register provider.")
        
        return provider
