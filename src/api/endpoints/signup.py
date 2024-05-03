from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db_session
from src.db.repositories import providers_repository
from src.api.models import ProviderRequestModel, WeakPasswordException
from src.api.constants import USERNAME_MIN_LENGTH
from src.api.utils.security import is_password_strong
from src.api.setup.logging import logger
from src.api.services.providers import ProviderService
from src.api.dependencies import get_provider_service

router = APIRouter(prefix="/api", tags=["auth"])

@router.post('/register')
async def signup(
    form_data: ProviderRequestModel,
    provider_service: ProviderService = Depends(get_provider_service),
    session: AsyncSession = Depends(get_db_session)
):    
    try:
        provider = await provider_service.register(form_data, session)

    except WeakPasswordException as e:
        logger.info(e.error)
        raise HTTPException(status_code=400, detail=e.error)

    return {"message": "Provider registered successfully!"}
