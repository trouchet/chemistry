from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from unittest.mock import patch
import pytest
from os import path

from src.app import app
from src.config import settings

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/db
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    engine = create_engine(
        settings.ASYNC_POSTGRES_URI_TEST, 
        echo=settings.POSTGRES_ECHO
    )
    yield engine
    engine.dispose()  # Close the connection after tests

@pytest.fixture(scope="function")
def session(engine):
    """Create a test database session."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()  # Close the session after each test


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/api/routes
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_get_client_data(mocker, sample_dataframe):
    return mocker.patch(
        'src.routes.recommendation.get_client_data',
        return_value=('order_id', 'item_id', 'description', sample_dataframe),
    )


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
## src/api/utils/native
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
@pytest.fixture
def sample_dict():
    return {'a': [1, 2, 3], 'b': [2, 4, 6], 'c': [3, 6, 9]}


@pytest.fixture
def mangled_sample_dict():
    # Value is not a list
    return {'a': [1, 2, 3], 'b': [2, 4, 6], 'c': {'foo': 'bar'}}


@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def mock_read_data_to_dataframe_gen():
    path = 'src.api.utils.dataframe.read_data_to_dataframe_gen'

    with patch(path) as mock_gen:
        yield mock_gen


@pytest.fixture
def pkl_filepath(tmp_path):
    return path.join(tmp_path, 'test.pkl')


@pytest.fixture
def dill_filepath(tmp_path):
    return path.join(tmp_path, 'test.dill')


@pytest.fixture
def cloudpickle_filepath(tmp_path):
    return path.join(tmp_path, 'test_cloudpickle.pkl')
