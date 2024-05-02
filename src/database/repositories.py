from typing import Annotated
from fastapi import Depends
from collections.abc import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from typing import TypeVar

from src.database.schemas import (
    Base,
    Provider,
    Companies,
    Product,
    TransactionHistory,
    TransactionHistoryFile,
    ProductPrediction
)
from src.database.session import get_db_session
from .base.repository import DatabaseRepository

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)  

class AsyncRepositoryFactory:
    def __init__(self, model: ModelType):
        self.model = model

    async def create_repository(self, session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(self.model, session)

# Repositórios
providers_repository = AsyncRepositoryFactory(Provider)
providers_clients_repository = AsyncRepositoryFactory(Companies)
products_repository = AsyncRepositoryFactory(Product)
TransactionHistoryRepository = AsyncRepositoryFactory(TransactionHistory)
transaction_history_files_repository = AsyncRepositoryFactory(TransactionHistoryFile)
product_predictions_repository = AsyncRepositoryFactory(ProductPrediction)
