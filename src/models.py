from pydantic import BaseModel
from typing import Optional

from os import environ

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
    items: str
    algorithm: Optional[str] = None

# Response model
class Recommendation(BaseModel):
    items: str
