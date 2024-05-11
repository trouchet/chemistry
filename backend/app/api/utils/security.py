from re import search
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import encode
from typing import Any, Union

from ... import settings
from ..constants import MIN_PASSWORD_LENGTH

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


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

    def and_map(x, y):
        return x and y

    return reduce(and_map, is_password_strong_dict(password).values())
