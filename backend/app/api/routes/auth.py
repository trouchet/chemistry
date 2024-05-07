from fastapi import APIRouter, Depends

from src.logging import logger
from src.models.users import UserRequest
from src.services.users import UserService
from src.dependencies.dependencies import get_user_service
from src.exceptions import WeakPasswordException

router = APIRouter(prefix="/api", tags=["auth"])

@router.post('/signup')
async def signup(
    form_data: UserRequest,
    provider_service: UserService = Depends(get_user_service)
):
    try:
        user = await provider_service.register(form_data)

    except WeakPasswordException as e:
        logger.info(e.error)
        return e

    return {
        "message": "Provider registered successfully!",
        "data": user.dict(),
    }
