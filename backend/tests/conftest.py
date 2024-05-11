from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from os import path

from backend.app import settings, app
from backend.app.db.base import engine, init_db
from backend.app.models import User
from .utils import authentication_token_from_email, get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session

        statement = delete(User)
        session.execute(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# src/api/routes
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_data():
    return {"data": 42}


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# src/api/utils/native
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_dict():
    return {"a": [1, 2, 3], "b": [2, 4, 6], "c": [3, 6, 9]}


@pytest.fixture
def mangled_sample_dict():
    # Value is not a list
    return {"a": [1, 2, 3], "b": [2, 4, 6], "c": {"foo": "bar"}}


@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def pkl_filepath(tmp_path):
    return path.join(tmp_path, "test.pkl")


@pytest.fixture
def dill_filepath(tmp_path):
    return path.join(tmp_path, "test.dill")
