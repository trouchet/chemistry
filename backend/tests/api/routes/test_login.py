from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session, select
from typing import Dict

from backend.app.core.config import settings
from backend.app.api.utils.security import verify_password
from backend.app.models.users import User
from backend.app.api.utils.email import generate_password_reset_token


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()

    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    route = f"{settings.API_V1_STR}/login/access-token"
    r = client.post(route, data=login_data)
    assert r.status_code == 400


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/login/test-token"
    r = client.post(route, headers=superuser_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_recovery_password(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    host_info = (
        "backend.app.core.config.settings.SMTP_HOST",
        "smtp.example.com",
    )
    user_info = (
        "backend.app.core.config.settings.SMTP_USER",
        "admin@example.com",
    )

    with patch(host_info[0], host_info[1]), patch(user_info[0], user_info[1]):
        email = "test@example.com"
        route = f"{settings.API_V1_STR}/password-recovery/{email}"
        r = client.post(route, headers=normal_user_token_headers)
        assert r.status_code == 200
        assert r.json() == {"message": "Password recovery email sent"}


def test_recovery_password_user_not_exits(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    email = "jVgQr@example.com"
    route = f"{settings.API_V1_STR}/password-recovery/{email}"
    r = client.post(
        route,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 404


def test_reset_password(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    token = generate_password_reset_token(email=settings.FIRST_SUPERUSER)
    data = {"new_password": "changethis", "token": token}
    route = f"{settings.API_V1_STR}/reset-password/"
    r = client.post(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    assert r.json() == {"message": "Password updated successfully"}

    user_query = select(User).where(User.email == settings.FIRST_SUPERUSER)
    user = db.exec(user_query).first()
    assert user
    assert verify_password(data["new_password"], user.hashed_password)

    token = generate_password_reset_token(email=settings.FIRST_SUPERUSER)
    data = {"new_password": settings.FIRST_SUPERUSER_PASSWORD, "token": token}
    route = f"{settings.API_V1_STR}/reset-password/"
    r = client.post(
        route,
        headers=superuser_token_headers,
        json=data,
    )


def test_reset_password_invalid_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    data = {"new_password": "changethis", "token": "invalid"}
    route = f"{settings.API_V1_STR}/reset-password/"

    r = client.post(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    response = r.json()

    assert "detail" in response
    assert r.status_code == 400
    assert response["detail"] == "Invalid token"
