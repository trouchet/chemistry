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
class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET
    authjwt_algorithm: str = JWT_ALGORITHM

class User(BaseModel):
    username: str
    password: str

# Request model
class Basket(BaseModel):
    items: List[str] = Field(default=[])
    algorithm: Optional[str] = RECOMMENDATION_ALGO_DEFAULT
    horizon: Optional[int] = N_BEST_NEIGHBORS_DEFAULT

# Response model
class Recommendation(BaseModel):
    items: Optional[List[str]] = []