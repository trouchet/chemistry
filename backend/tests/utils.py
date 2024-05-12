import random
import string

from typing import Dict
from fastapi.testclient import TestClient
from sqlmodel import Session

from backend.app import settings
from backend.app.api.services.users import (
    create_user,
    get_user_by_email,
    update_user,
)
from backend.app.models.users import User, UserCreate, UserUpdate

EMAIL_LEN = 5


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=EMAIL_LEN))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()

    user_in = UserCreate(email=email, password=password)
    user = create_user(session=db, user_create=user_in)
    return user


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    route = f"{settings.API_V1_STR}/login/access-token"
    r = client.post(route, data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return user_authentication_headers(
        client=client,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = get_user_by_email(session=db, email=email)

    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = create_user(session=db, user_create=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)

        if not user.id:
            raise Exception("User id not set")
        user = update_user(session=db, db_user=user, user_in=user_in_update)

    return user_authentication_headers(client=client, email=email, password=password)
