from fastapi import HTTPException
from src.utils.security import is_password_strong_dict
from src import (
    USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH
)

class CredentialsException(HTTPException):
    def __init__(self):
        self.status_code=401,
        self.detail="Could not validate credentials"
        self.headers={"WWW-Authenticate": "Bearer"}

class WeakPasswordException(HTTPException):
    error: str = ""

    def __init__(self, password: str):
        super().__init__(self.error)

        # Password validation
        password_check_dict = is_password_strong_dict(password)

        warning_message="Password does not meet security requirements."
        advice_message=f"Check it out: {password_check_dict}."
        self.error = f"{warning_message} {advice_message}"

class UserAlreadyExistsException(HTTPException):
    def __init__(self, username: str):
        self.status_code=400
        self.detail=f"User with username {username} already exists."

class InvalidUsernameException(HTTPException):
    def __init__(self, username: str):
        min_msg=f"at least {USERNAME_MIN_LENGTH} characters"
        max_msg=f"at most {USERNAME_MAX_LENGTH} characters" 
        err_msg = f"User username must be {min_msg} and {max_msg}."
        
        self.status_code=400
        self.detail=f"Invalid username: {username}. {err_msg}."

class NonMatchingPasswordsException(HTTPException):
    def __init__(self):
        self.status_code=400
        self.detail=f"Provided password does not match the user's password."

class UserRegistrationException(HTTPException):
    def __init__(self, e: Exception):
        self.status_code=500
        self.detail="Failed to register user: {e}"