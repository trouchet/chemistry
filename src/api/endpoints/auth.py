from fastapi import APIRouter, HTTPException
from src.api.models import ProviderRequestModel
from src.api.services.providers import register_provider
from src.api.models import ProviderRequestModel
from src.database.repositories import providers_repository

router = APIRouter(prefix="/api", tags=["auth"])

# Continua ... 
# https://github.com/BadassHenkka/improvement-api
@router.post('/register')
async def signup(form_data: ProviderRequestModel):
    provider_exists = await providers_repository.get()
    
    if provider_exists:
        raise HTTPException(status_code=400, detail="This username is already taken.")

    if len(form_data.username) < 3:
        raise HTTPException(status_code=400, detail="The username needs to be at least 3 characters.")
    
    register_provider(form_data)

    {"message": "Provider registered successfully!"}
    return 
