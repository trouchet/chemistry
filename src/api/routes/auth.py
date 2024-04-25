from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["auth"])

TOKEN_EXPIRATION_MINUTES = 60

'''
from fastapi import Depends
# Change from library 'fastapi_jwt_auth' to 'fastapi.security' or 'jwt' 
# from fastapi_jwt_auth import AuthJWT
# Provides a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@router.post('/token')
def login(user: User, Authorize: AuthJWT = Depends()):
    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}
'''
