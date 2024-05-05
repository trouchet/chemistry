# Description: Models for the API.
from . import APIModel

# Providers request model
class UserRequest(APIModel):
    username: str
    password: str
