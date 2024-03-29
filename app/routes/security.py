from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.jwt import create_access_token, authenticate_user
from fastapi.security import OAuth2PasswordBearer

from app.models import Token

jwt_router = APIRouter()

# Fill here with the necessary jwt utils and routes
