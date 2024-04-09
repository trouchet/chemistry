from pydantic import BaseModel, Field
from typing import Optional, List
from os import environ

from src.core.recommendation.constants import N_BEST_NEIGHBORS_DEFAULT, \
    RECOMMENDATION_ALGO_DEFAULT

# JWT Secret and Algorithm
JWT_SECRET = str(environ.get('JWT_SECRET'))
JWT_ALGORITHM = str(environ.get('JWT_ALGORITHM')) 
    
# In production, you can use Settings management
# from pydantic to get secret key from .env
class JWTSettings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET
    authjwt_algorithm: str = JWT_ALGORITHM

# Request model
class User(BaseModel):
    username: str
    password: str

# Response model
class ErrorResponse(BaseModel):
    error: str

# Response model
class MessageResponse(BaseModel):
    message: str