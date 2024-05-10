from fastapi import HTTPException
from .utils.security import is_password_strong_dict
from .constants import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH
from ..db.types import PrimaryKeyType

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


class UserNotFoundException(HTTPException):
    def __init__(self, username: str):
        self.status_code=403
        self.detail=f"User {username} not found"
        

class InactiveUserException(HTTPException):
    def __init__(self, username: str):
        self.status_code=400
        self.detail=f"Inactive user"


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

class InexistentUserByIDException(HTTPException):
    def __init__(self, user_id: PrimaryKeyType):
        self.status_code=403
        self.detail=f"The user with id {user_id} does not exist in the system"

class InexistentUserByEmailException(HTTPException):
    def __init__(self, email: str):
        self.status_code=404
        self.detail="The user with email {email} does not exist in the system."

class WrongCredentialsException(HTTPException):
    def __init__(self):
        self.status_code=400
        self.detail="Incorrect email or password"

class InvalidTokenException(HTTPException):
    def __init__(self, e: Exception):
        self.status_code=400
        self.detail="Invalid token"
