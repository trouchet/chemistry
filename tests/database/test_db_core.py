import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from unittest.mock import AsyncMock, MagicMock

from src.database.base.repository import (
    BaseRepository,
    DatabaseRepository,
    RepositoryException,
)

from src.database.repositories import (
    providers_repository
)

class TestBaseRepository:
    @pytest.mark.abstract
    def test_is_abstract(self):
        with pytest.raises(TypeError):
            BaseRepository()


class TestDatabaseRepository:
    @pytest.mark.asyncio
    async def test_get_success(self, mocker):
        # Mock session and model
        session = AsyncMock()
        model = MagicMock()
        pk = 1

        # Create repository and call get
        repository = DatabaseRepository(model)
        entity = await repository.find_by_id(pk, session)

        # Assertions
        assert entity == model
        session.get.assert_called_once_with(model, pk)

    @pytest.mark.asyncio
    async def test_find_failure(self, mocker):
        # Mock session and model
        session = AsyncMock()
        model = MagicMock()
        pk = 1
        error = SQLAlchemyError("Something went wrong")

        # Mock failed retrieval and patch model.__name__
        model.__name__ = "TestModel"  # Patch the attribute

        # Create repository and expect exception
        repository = DatabaseRepository(model)
        with pytest.raises(RepositoryException) as excinfo:
            await repository.find_by_id(pk, session)

        # Assertion uses the patched attribute
        assert f"Failed to find {model.__name__} by id {pk}" in str(excinfo.value)
        session.get.assert_called_once_with(model, pk)

    @pytest.mark.asyncio
    async def test_save_success(self, mocker):
        # Mock session and model
        session = AsyncMock()
        model = MagicMock()
        data = {"name": "Test Data"}

        # Create repository and call create
        repository = DatabaseRepository(model)
        
        created_entity = await repository.save(model, session)

        # Assertions
        # Assuming session.add was called with specific arguments
        session.add.assert_called_once_with(model)

        # Assuming other methods were called as expected
        session.commit.assert_called_once_with()
        session.refresh.assert_called_once_with(model)
