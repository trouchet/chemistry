from fastapi import HTTPException
from .api.utils.security import is_password_strong_dict
from .api.constants import USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH


# Custom exceptions
class CredentialsException(HTTPException):
    def __init__(self):
        self.status_code = (401,)
        self.detail = "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}


class WrongCredentialsException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Incorrect username or password"


class OpenRegistrationForbiddenException(HTTPException):
    def __init__(self):
        self.status_code = 403
        self.detail = "Open user registration is forbidden on this server"


class InsufficientPrivilegesException(HTTPException):
    def __init__(self):
        self.status_code = 403
        self.detail = "The user doesn't have enough privileges"


# Password exceptions
class WeakPasswordException(HTTPException):
    error: str = ""

    def __init__(self, password: str):
        super().__init__(self.error)

        # Password validation
        password_check_dict = is_password_strong_dict(password)

        warning_message = "Password does not meet security requirements."
        advice_message = f"Check it out: {password_check_dict}."
        self.error = f"{warning_message} {advice_message}"


class NonMatchingPasswordsException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Provided password does not match the user's password."


class WrongPasswordException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Incorrect password"


class SamePreviousPasswordException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "New password cannot be the same as the current one"


class UserNotFoundException(HTTPException):
    def __init__(self, username: str):
        self.status_code = 403
        self.detail = f"User {username} not found"


# Users exceptions
class InactiveUserException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Inactive user"


class UserAlreadyExistsByUsernameException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "User with this username already exists in the system."


class UserAlreadyExistsByEMailException(HTTPException):
    def __init__(self):
        self.status_code = 409
        self.detail = "User with this email already exists in the system."


class InvalidUsernameException(HTTPException):
    def __init__(self, username: str):
        min_msg = f"at least {USERNAME_MIN_LENGTH} characters"
        max_msg = f"at most {USERNAME_MAX_LENGTH} characters"
        err_msg = f"User username must be {min_msg} and {max_msg}."

        self.status_code = 400
        self.detail = f"Invalid username: {err_msg}."


class InvalidEmailException(HTTPException):
    def __init__(self, email: str):
        self.status_code = 400
        self.detail = f"Invalid email: {email}."


class UserRegistrationException(HTTPException):
    def __init__(self, e: Exception):
        self.status_code = 500
        self.detail = "Failed to register user: {e}"


class InexistentUserException(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User not found"


class InexistentUserByUsernameException(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "The user with this id does not exist in the system"


class InexistentUserByIDException(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "The user with this id does not exist in the system"


class InexistentUserByEmailException(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "The user with email does not exist in the system."


class SuperUserForbiddenException(HTTPException):
    def __init__(self):
        self.status_code = 403
        self.detail = "Super users are not allowed to delete themselves"


# Token exceptions
class InvalidTokenException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Invalid token"
