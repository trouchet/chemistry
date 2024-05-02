from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


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
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = pyjwt.encode(
        payload={**to_encode, "exp": expire.timestamp()},  # Combine data and expiration
        secret_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt
