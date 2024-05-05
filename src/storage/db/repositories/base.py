from abc import ABC, abstractmethod
from typing import List, Any
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select

from src.storage.db.base.exceptions import RepositoryException
from src.storage.db.base.types import Model, PrimaryKeyType

class BaseRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Model]:
        pass

    @abstractmethod
    def find_by_id(self, pk: PrimaryKeyType) -> Model:
        pass

    @abstractmethod
    def save(self, entity: Model) -> Model:
        pass

    @abstractmethod
    def exists_by_id(self, id: PrimaryKeyType) -> bool:
        pass

    @abstractmethod
    def delete_by_id(self, id: PrimaryKeyType) -> None:
        pass


def fail_message(action, e):
    return f"Failed to {action}: {e}"

class SQLRepository(BaseRepository):
    def __init__(self, model: Model, session: AsyncSession) -> None:
        self.session = session
        self.model = model
        self.model_name = model.__class__.__name__

    async def __raise_repository_exception(self, action: str, e: Exception) -> None:
        fail_message = f"Failed to {action}: {e}"
        raise RepositoryException(fail_message)

    async def find_all(self) -> List[Model]:
        try:
            # Await the coroutine to get the data list
            query_result = await self.session.execute(select(self.model))
            data = query_result.scalars().all()
            return data
        except SQLAlchemyError as e:
            action = f'find all {self.model_name}'
            await self.__raise_repository_exception(action, e)

    async def find_by_id(
        self, pk: PrimaryKeyType
    ) -> Optional[Model]:

        try:
            data = await self.session.get(self.model, pk)
            return data
        except SQLAlchemyError as e:
            action = f'find {self.model_name} by id {pk}'
            await self.__raise_repository_exception(action, e)

    async def exists_by_id(self, pk: PrimaryKeyType) -> bool:
        try:
            entity = await self.session.get(self.model, pk)
            return entity is not None
        except SQLAlchemyError as e:
            action = f'check existence of {self.model_name} by id {pk}'
            await self.__raise_repository_exception(action, e)

    async def delete_by_id(self, pk: PrimaryKeyType) -> None:
        try:
            entity = await self.session.get(self.model, pk)
            if entity is not None:
                self.session.delete(entity)
                await self.session.commit()
        except SQLAlchemyError as e:
            action = f'delete {self.model_name} by id {pk}'
            await self.__raise_repository_exception(action, e)

    async def save(self, entity: Model) -> Model:
        try:
            await self.session.add(entity)
            await self.session.commit()
            await self.session.refresh(entity)
            return entity

        except SQLAlchemyError as e:
            action = f'save {self.model_name}'
            await self.__raise_repository_exception(action, e)

    async def filter_by_field(
        self, field: str, value: Any
    ) -> Optional[List[Model]]:
        try:
            field_value = getattr(self.model, field) == value
            query = select(self.model).filter(field_value)
            
            # Use await session.execute(query) for fetching data
            data = await self.session.execute(query)
               
            # Use data.scalars().all() to get the actual data list
            return data.fetchall()
        
        except SQLAlchemyError as e:
            action = f"filter {self.model_name} by field {field}={value}"
            await self.__raise_repository_exception(action, e)

