from fastapi import APIRouter, HTTPException, Depends

from src.models import ProviderRequestModel, WeakPasswordException
from src.setup.logging import logger
from src.services.models.users import UserService
from src.services.dependencies import get_user_service

router = APIRouter(prefix="/api", tags=["auth"])


@router.post('/signup')
async def signup(
    form_data: ProviderRequestModel,
    provider_service: UserService = Depends(get_user_service)
):
    try:
        user = await provider_service.register(form_data)

    except WeakPasswordException as e:
        logger.info(e.error)
        raise HTTPException(status_code=400, detail=e.error)

    return {"message": "Provider registered successfully!"}
