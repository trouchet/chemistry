from fastapi import APIRouter

from . import setup, login, utils, users

api_router = APIRouter()

# Add routers here
api_router.include_router(setup.router, tags=["setup"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
