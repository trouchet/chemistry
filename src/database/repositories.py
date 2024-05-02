from typing import Annotated
from fastapi import Depends
from collections.abc import Callable
from sqlalchemy.ext.asyncio import AsyncSession

from database import schemas, session
from database.base.repository import DatabaseRepository

def get_repository(
    model: type[schemas.Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(session.get_db_session)):
        return DatabaseRepository(model, session)

    return func

def create_repository(model):
    return Annotated[
        DatabaseRepository[model],
        Depends(get_repository(model)),
    ]

# Repositórios
providers_repository = create_repository(schemas.Provider)
providers_clients_repository = create_repository(schemas.Companies)
products_repository = create_repository(schemas.Product)
TransactionHistoryRepository = create_repository(schemas.TransactionHistory)
transaction_history_files_repository = create_repository(schemas.TransactionHistoryFile)
product_predictions_repository = create_repository(schemas.ProductPrediction)
