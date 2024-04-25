from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List, TypeVar
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Base, PRIMARY_KEY_TYPE

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import models, repositories, session

Model = TypeVar("Model", bound= Base)

class BaseRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Model]:
        pass

    @abstractmethod
    def save(self, entity: Model) -> Model:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Model:
        pass

    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        pass

class RepositoryException(Exception):
    pass

def fail_message(action, e):
    return f"Failed to {action}: {e}"

class DatabaseRepository(BaseRepository):
        def __init__(self, model: type[Model], session: AsyncSession) -> None:
            self.model = model
            self.session = session
        
        async def get(self, pk: PRIMARY_KEY_TYPE) -> Model:
            try:
                return await self.session.get(self.model, pk)

            except SQLAlchemyError as e:
                action = f'find {self.model.__name__} by id {id}'
                fail_find_message = fail_message(action, e)
                raise RepositoryException(fail_find_message)

        async def find_all(self) -> List[Model]:
            try:
                return await self.session.query(self.model).all()
            
            except SQLAlchemyError as e:
                fail_find_all_message = f"Failed to find all {self.model.__name__}: {e}"
                raise RepositoryException(fail_find_all_message)

        async def create(self, data: dict) -> Model:
            try:
                instance = self.model(**data)
                self.session.add(instance)
                await self.session.commit()
                await self.session.refresh(instance)
                return instance
            
            except SQLAlchemyError as e:
                action = f'save {self.model.__name__}'
                fail_save_message = fail_message(action, e)
                raise RepositoryException(fail_save_message)

        async def exists(self, pk: PRIMARY_KEY_TYPE) -> bool:
            try:
                entity = await self.session.get(self.model, pk)
                return entity is not None

            except SQLAlchemyError as e:
                action = f'check existence of {self.model.__name__} by id {id}'
                fail_check_message = fail_message(action, e)
                raise RepositoryException(fail_check_message)

        async def delete(self, pk: PRIMARY_KEY_TYPE) -> None:
            try:
                entity = await self.session.get(self.model, pk)
                if entity is not None:
                    self.session.delete(entity)
                    self.session.commit()
            
            except SQLAlchemyError as e:
                action = f'delete {self.model.__name__} by id {id}'
                fail_delete_message = fail_message(action, e)
                raise RepositoryException(fail_delete_message)
