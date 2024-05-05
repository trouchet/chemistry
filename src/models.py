# 
from pydantic import BaseModel

# Providers request model
class UserRequest(BaseModel):
    username: str
    password: str
