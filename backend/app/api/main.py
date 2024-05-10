from fastapi import APIRouter

from .routes import setup, login, file, utils, users

api_router = APIRouter()

# Add routers here
api_router.include_router(setup.router)
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(file.router)
api_router.include_router(utils.router)
