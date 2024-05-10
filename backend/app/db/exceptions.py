from fastapi import HTTPException

class UserNotFoundException(HTTPException):
    def __init__(self, username: str):
        self.status_code=404
        self.detail=f"User with username {username} not found."

class InvalidEmailException(HTTPException):
    def __init__(self, email: str):
        self.status_code=400
        self.detail=f"Invalid email: {email}." 
