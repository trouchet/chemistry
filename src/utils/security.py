from re import search
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import encode, decode

from src.config import settings
from src.constants import MIN_PASSWORD_LENGTH

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def is_password_strong_dict(password: str) -> bool:
    """
    Checks if a password meets minimum security requirements.

    Args:
        password (str): The password to be checked.

    Returns:
        dict: A dictionary with the requirements and whether they are met.
    """

    has_lowercase = search(r"[a-z]", password)
    has_uppercase = search(r"[A-Z]", password)
    has_number = search(r"\d", password)
    has_special_char = search(r"[^\w\s]", password)

    return {
        "min_length": len(password) >= MIN_PASSWORD_LENGTH,
        "has_lowercase": bool(has_lowercase),
        "has_uppercase": bool(has_uppercase),
        "has_number": bool(has_number),
        "has_special_char": bool(has_special_char),
    }


def is_password_strong(password: str) -> bool:
    """
    Checks if a password meets minimum security requirements.

    Args:
        password (str): The password to be checked.

    Returns:
        bool: True if the password is strong, False otherwise.
    """
    from functools import reduce

    and_map = lambda x, y: x and y
    return reduce(and_map, is_password_strong_dict(password).values())


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Creates an access token using PyJWT.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta], optional): An optional timedelta for token expiration. Defaults to None.

    Returns:
        str: The encoded access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    encoded_jwt = encode(
        {**to_encode, "exp": expire.timestamp()},
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def decode_jwt(token: str):
    return decode(
        token, 
        settings.SECRET_KEY, 
        algorithms=[settings.JWT_ALGORITHM]
    )