from fastapi import HTTPException

class CredentialsException(HTTPException):
    def __init__(self):
        self.status_code=401,
        self.detail="Could not validate credentials"
        self.headers={"WWW-Authenticate": "Bearer"}