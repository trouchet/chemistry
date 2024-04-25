from pydantic import BaseModel
from os import environ

# JWT Secret and Algorithm
JWT_SECRET = str(environ.get('JWT_SECRET'))
JWT_ALGORITHM = str(environ.get('JWT_ALGORITHM'))


# In production, you can use Settings management
# from pydantic to get secret key from .env
class JWTSettings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET
    authjwt_algorithm: str = JWT_ALGORITHM


# Response model
class ErrorResponse(BaseModel):
    error: str


# Response model
class MessageResponse(BaseModel):
    message: str
