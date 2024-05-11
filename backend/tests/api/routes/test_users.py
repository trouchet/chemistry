from unittest.mock import patch

from fastapi.testclient import TestClient
from typing import Dict
from sqlmodel import Session, select

from app.api.services.users import create_user, get_user_by_email
from backend.app import settings
from backend.app.api.utils.security import verify_password
from backend.app.models import User, UserCreate

from backend.tests.utils import random_email, random_lower_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/users/me"
    r = client.get(route, headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/users/me"
    r = client.get(route, headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    with (
        patch("app.utils.send_email", return_value=None),
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        username = random_email()
        password = random_lower_string()

        route = f"{settings.API_V1_STR}/users/"
        data = {"email": username, "password": password}
        r = client.post(
            route,
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = get_user_by_email(session=db, email=username)
        assert user
        assert user.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)
    user_id = user.id

    route = f"{settings.API_V1_STR}/users/{user_id}"
    r = client.get(route, headers=superuser_token_headers)
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = get_user_by_email(session=db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_current_user(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)
    user_id = user.id

    login_data = {
        "username": username,
        "password": password,
    }

    route = f"{settings.API_V1_STR}/login/access-token"
    r = client.post(route, data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    route = f"{settings.API_V1_STR}/users/{user_id}"
    r = client.get(
        route,
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = get_user_by_email(session=db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_permissions_error(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/users/999999"
    r = client.get(
        route,
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "The user doesn't have enough privileges"}


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    create_user(session=db, user_create=user_in)

    route = f"{settings.API_V1_STR}/users/"
    data = {"email": username, "password": password}
    r = client.post(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    route = f"{settings.API_V1_STR}/users/"

    r = client.post(
        route,
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


def test_retrieve_users(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    create_user(session=db, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    create_user(session=db, user_create=user_in2)

    route = f"{settings.API_V1_STR}/users/"
    r = client.get(route, headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users["data"]) > 1
    assert "count" in all_users
    for item in all_users["data"]:
        assert "email" in item


def test_update_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    full_name = "Updated Name"
    email = random_email()
    data = {"full_name": full_name, "email": email}
    route = f"{settings.API_V1_STR}/users/me"

    r = client.patch(
        route,
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 200

    updated_user = r.json()
    assert updated_user["email"] == email
    assert updated_user["full_name"] == full_name

    user_query = select(User).where(User.email == email)
    user_db = db.exec(user_query).first()
    assert user_db
    assert user_db.email == email
    assert user_db.full_name == full_name


def test_update_password_me(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    new_password = random_lower_string()
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": new_password,
    }
    route = f"{settings.API_V1_STR}/users/me/password"
    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200

    updated_user = r.json()
    assert updated_user["message"] == "Password updated successfully"

    user_query = select(User).where(User.email == settings.FIRST_SUPERUSER)
    user_db = db.exec(user_query).first()
    assert user_db
    assert user_db.email == settings.FIRST_SUPERUSER
    assert verify_password(new_password, user_db.hashed_password)

    # Revert to the old password to keep consistency in test
    old_data = {
        "current_password": new_password,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    route = f"{settings.API_V1_STR}/users/me/password"

    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=old_data,
    )
    db.refresh(user_db)

    assert r.status_code == 200
    assert verify_password(settings.FIRST_SUPERUSER_PASSWORD, user_db.hashed_password)


def test_update_password_me_incorrect_password(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    new_password = random_lower_string()
    data = {"current_password": new_password, "new_password": new_password}
    route = f"{settings.API_V1_STR}/users/me/password"

    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400

    updated_user = r.json()
    assert updated_user["detail"] == "Incorrect password"


def test_update_user_me_email_exists(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)

    route = f"{settings.API_V1_STR}/users/me"
    data = {"email": user.email}
    r = client.patch(
        route,
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


def test_update_password_me_same_password_error(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/users/me/password"
    data = {
        "current_password": settings.FIRST_SUPERUSER_PASSWORD,
        "new_password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 400

    updated_user = r.json()
    assert (
        updated_user["detail"] == "New password cannot be the same as the current one"
    )


def test_register_user(client: TestClient, db: Session) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        username = random_email()
        password = random_lower_string()
        full_name = random_lower_string()

        route = f"{settings.API_V1_STR}/users/signup"
        data = {"email": username, "password": password, "full_name": full_name}

        r = client.post(
            route,
            json=data,
        )
        assert r.status_code == 200

        created_user = r.json()
        assert created_user["email"] == username
        assert created_user["full_name"] == full_name

        user_query = select(User).where(User.email == username)
        user_db = db.exec(user_query).first()
        assert user_db
        assert user_db.email == username
        assert user_db.full_name == full_name
        assert verify_password(password, user_db.hashed_password)


def test_register_user_forbidden_error(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", False):
        username = random_email()
        password = random_lower_string()
        full_name = random_lower_string()

        route = f"{settings.API_V1_STR}/users/signup"
        data = {"email": username, "password": password, "full_name": full_name}

        r = client.post(
            route,
            json=data,
        )
        assert r.status_code == 403
        assert (
            r.json()["detail"] == "Open user registration is forbidden on this server"
        )


def test_register_user_already_exists_error(client: TestClient) -> None:
    with patch("app.core.config.settings.USERS_OPEN_REGISTRATION", True):
        password = random_lower_string()
        full_name = random_lower_string()

        route = f"{settings.API_V1_STR}/users/signup"
        data = {
            "email": settings.FIRST_SUPERUSER,
            "password": password,
            "full_name": full_name,
        }
        r = client.post(
            route,
            json=data,
        )
        assert r.status_code == 400
        assert (
            r.json()["detail"]
            == "The user with this email already exists in the system"
        )


def test_update_user(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)

    route = f"{settings.API_V1_STR}/users/{user.id}"
    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=data,
    )

    assert r.status_code == 200
    updated_user = r.json()

    assert updated_user["full_name"] == "Updated_full_name"

    user_query = select(User).where(User.email == username)
    user_db = db.exec(user_query).first()
    db.refresh(user_db)
    assert user_db
    assert user_db.full_name == "Updated_full_name"


def test_update_user_not_exists(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    data = {"full_name": "Updated_full_name"}

    route = f"{settings.API_V1_STR}/users/99999999"
    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=data,
    )

    expected_message = "The user with this id does not exist in the system"
    assert r.status_code == 404
    assert r.json()["detail"] == expected_message


def test_update_user_email_exists(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user2 = create_user(session=db, user_create=user_in2)

    route = f"{settings.API_V1_STR}/users/{user.id}"
    data = {"email": user2.email}
    r = client.patch(
        route,
        headers=superuser_token_headers,
        json=data,
    )
    expected_message = "User with this email already exists"

    assert r.status_code == 409
    assert r.json()["detail"] == expected_message


def test_delete_user_me(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)
    user_id = user.id

    login_data = {
        "username": username,
        "password": password,
    }
    route = f"{settings.API_V1_STR}/login/access-token"
    r = client.post(route, data=login_data)

    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    route = f"{settings.API_V1_STR}/users/me"
    r = client.delete(
        route,
        headers=headers,
    )
    assert r.status_code == 200

    expected_message = "User deleted successfully"
    deleted_user = r.json()
    assert deleted_user["message"] == expected_message

    result = db.exec(select(User).where(User.id == user_id)).first()
    assert result is None

    user_query = select(User).where(User.id == user_id)
    user_db = db.execute(user_query).first()
    assert user_db is None


def test_delete_user_me_as_superuser(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    route = f"{settings.API_V1_STR}/users/me"
    r = client.delete(
        route,
        headers=superuser_token_headers,
    )
    assert r.status_code == 403

    expected_message = "Super users are not allowed to delete themselves"
    response = r.json()
    assert response["detail"] == expected_message


def test_delete_user_super_user(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)
    user_id = user.id
    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200

    expected_message = "User deleted successfully"
    deleted_user = r.json()
    assert deleted_user["message"] == expected_message

    result = db.exec(select(User).where(User.id == user_id)).first()
    assert result is None


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/users/99999999",
        headers=superuser_token_headers,
    )

    expected_message = "User not found"
    assert r.status_code == 404
    assert r.json()["detail"] == expected_message


def test_delete_user_current_super_user_error(
    client: TestClient, superuser_token_headers: Dict[str, str], db: Session
) -> None:
    super_user = get_user_by_email(session=db, email=settings.FIRST_SUPERUSER)
    assert super_user
    user_id = super_user.id

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )

    expected_message = "Super users are not allowed to delete themselves"
    assert r.status_code == 403
    assert r.json()["detail"] == expected_message


def test_delete_user_without_privileges(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()

    user_in = UserCreate(email=username, password=password)
    user = create_user(session=db, user_create=user_in)

    r = client.delete(
        f"{settings.API_V1_STR}/users/{user.id}",
        headers=normal_user_token_headers,
    )

    expected_message = "The user doesn't have enough privileges"
    assert r.status_code == 403
    assert r.json()["detail"] == expected_message
