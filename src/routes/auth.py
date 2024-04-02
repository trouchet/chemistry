from fastapi import APIRouter, Depends
# from fastapi_jwt_auth import AuthJWT

from src.models import User

router = APIRouter()

# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
'''
@router.post('/token')
def login(user: User, Authorize: AuthJWT = Depends()):
    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}
'''