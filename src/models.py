from pydantic import BaseModel

'''
from os import environ
from fastapi_jwt_auth import AuthJWT

JWT_SECRET = str(environ.get('JWT_SECRET'))
JWT_ALGORITHM = str(environ.get('JWT_ALGORITHM')) 
    
# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = JWT_SECRET

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()
'''

class User(BaseModel):
    username: str
