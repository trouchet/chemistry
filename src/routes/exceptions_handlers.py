# exception_handlers.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return {"detail": exc.detail}

@router.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return {"detail": "Internal server error"}