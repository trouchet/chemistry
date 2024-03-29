from fastapi import APIRouter
from datetime import timedelta

from src.services.jwt import create_access_token

router = APIRouter()

@router.post("/token")
async def get_access_token():
    # Assume this is the data you want to encode in the token
    data = {"username": "example_user"}

    # Generate an access token with a 30-minute expiration
    access_token = create_access_token(data, timedelta(minutes=30))

    # Return the access token in the response
    return {"access_token": access_token, "token_type": "bearer"}