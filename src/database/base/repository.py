from abc import ABC, abstractmethod
from typing import List, TypeVar
from typing import Union
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select

from src.database.schemas import Base
from src.database.session import get_db_session
from fastapi import Depends

PrimaryKeyType = Union[int, str, UUID]
Model = TypeVar("Model", bound= Base)

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

class RepositoryException(Exception):
    pass

def fail_message(action, e):
    return f"Failed to {action}: {e}"

class DatabaseRepository(BaseRepository):
        def __init__(self, model: type[Model]) -> None:
            self.model = model
            self.model_name = model.__class__.__name__
        
        async def find_all(
            self,
            session: AsyncSession
        ) -> List[Model]:
            try:
                # Await the coroutine to get the data list
                query_result = await session.execute(select(self.model))
                data = query_result.scalars().all()
                return data
            except SQLAlchemyError as e:
                fail_find_all_message = f"Failed to find all {self.model_name}: {e}"
                raise RepositoryException(fail_find_all_message)

        async def find_by_id(
            self, 
            pk: PrimaryKeyType,
            session: AsyncSession
        ) -> Optional[Model]:
            try:
                return await session.get(self.model, pk)
            except SQLAlchemyError as e:
                action = f'find {self.model_name} by id {pk}'
                fail_find_message = fail_message(action, e)
                raise RepositoryException(fail_find_message)
        
        async def exists_by_id(
            self, 
            pk: PrimaryKeyType,
            session: AsyncSession
        ) -> bool:
            try:
                entity = await session.get(self.model, pk)
                return entity is not None
            except SQLAlchemyError as e:
                action = f'check existence of {self.model_name} by id {pk}'
                fail_check_message = fail_message(action, e)
                raise RepositoryException(fail_check_message)

    
        async def delete_by_id(
            self, 
            pk: PrimaryKeyType,
            session: AsyncSession
        ) -> None:
            try:
                entity = await session.get(self.model, pk)
                if entity is not None:
                    session.delete(entity)
                    await session.commit()
            except SQLAlchemyError as e:
                action = f'delete {self.model_name} by id {pk}'
                fail_delete_message = fail_message(action, e)
                raise RepositoryException(fail_delete_message)

        async def save(
            self, 
            entity: Model, 
            session: AsyncSession
        ) -> Model:
            try:            
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
                return entity
            
            except SQLAlchemyError as e:
                action = f'save {self.model_name}'
                fail_save_message = fail_message(action, e)
                raise RepositoryException(fail_save_message)
            
        async def find_by_filters(
            self,
            filters: dict,
            session: AsyncSession
        ) -> List[Model]:
            try:
                query = select(self.model)
                for key, value in filters.items():
                    # Assuming key is the column name and value is the filter value
                    query = query.filter(getattr(self.model, key) == value)
                
                data = await query.fetch_all()  # Use fetch_all if available
                return data
            except SQLAlchemyError as e:
                action = f'find {self.model_name} by filters: {e}'
                fail_save_message = fail_message(action, e)
                fail_message = f"Failed to "
                raise RepositoryException(fail_message)

