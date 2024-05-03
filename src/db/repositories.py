from typing import TypeVar

from src.db.schemas import (
    Base,
    Provider,
    Companies,
    Product,
    TransactionHistory,
    TransactionHistoryFile,
    ProductPrediction
)
from .base.repository import DatabaseRepository

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)  

# Repositórios
providers_repository = DatabaseRepository(Provider)
providers_clients_repository = DatabaseRepository(Companies)
products_repository = DatabaseRepository(Product)
TransactionHistoryRepository = DatabaseRepository(TransactionHistory)
transaction_history_files_repository = DatabaseRepository(TransactionHistoryFile)
product_predictions_repository = DatabaseRepository(ProductPrediction)

