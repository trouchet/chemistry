from fastapi import APIRouter, Depends

from src.logging import logger
from src.models.users import UserRequest
from src.services.users import UserService
from src.dependencies.services import UserServiceDependency
from src.exceptions import WeakPasswordException

router = APIRouter(prefix="/api", tags=["auth"])

@router.post('/signup')
async def signup(
    form_data: UserRequest,
    provider_service: UserServiceDependency
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
