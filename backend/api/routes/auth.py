from fastapi import APIRouter, Depends

from backend.core.logging import logger
from backend.api.models.users import UserRequest
from backend.api.dependencies.services import UserServiceDependency
from backend.services.users import UserService
from backend.exceptions import WeakPasswordException

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
