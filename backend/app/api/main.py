from fastapi import APIRouter

from .routes import auth, setup, file

api_router = APIRouter()

# Add routers here
api_router.include_router(setup.router)
api_router.include_router(auth.router)
api_router.include_router(file.router)