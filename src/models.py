from pydantic import BaseModel
from typing import List
from os import environ
from fastapi_jwt_auth import AuthJWT

JWT_SECRET = str(environ.get('JWT_SECRET'))
JWT_ALGORITHM = str(environ.get('JWT_ALGORITHM')) 

class User(BaseModel):
    username: str
    
# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# Request model
class BasketRequest(BaseModel):
    basket: List[str]

# Response model
class RecommendationResponse(BaseModel):
    recommendation: str