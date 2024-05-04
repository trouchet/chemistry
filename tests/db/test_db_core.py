import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from unittest.mock import AsyncMock, MagicMock

from src.db.base.repository import (
    BaseRepository,
    SQLRepository,
    RepositoryException,
)

class TestBaseRepository:
    def test_is_abstract(self):
        with pytest.raises(TypeError):
            BaseRepository()


class TestSQLRepository:
    @pytest.mark.asyncio
    async def test_get_success(self, mocker):
        # Mock session and model
        session = AsyncMock()
        model = MagicMock()
        pk = 1

        # Create repository and call get
        repository = SQLRepository(model)
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
        
        # Mock session.get to raise exception
        session.get.side_effect = RepositoryException("Mocked exception")
        
        # Create repository and expect exception
        repository = SQLRepository(model)
        with pytest.raises(RepositoryException) as excinfo:
            await repository.find_by_id(pk, session)
        
        # Assertion not needed as exception message is mocked
        session.get.assert_called_once_with(model, pk)

    @pytest.mark.asyncio
    async def test_save_success(self, mocker):
        # Mock session and model
        session = AsyncMock()
        model = MagicMock()
        data = {"name": "Test Data"}

        # Create repository and call create
        repository = SQLRepository(model)
        
        await repository.save(model, session)

        # Assertions
        # Assuming session.add was called with specific arguments
        session.add.assert_called_once_with(model)

        # Assuming other methods were called as expected
        session.commit.assert_called_once_with()
        session.refresh.assert_called_once_with(model)
