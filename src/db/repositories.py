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
from .base.repository import SQLRepository

# Generic type for model
ModelType = TypeVar("ModelType", bound=Base)  

# Repositórios
providers_repository = SQLRepository(Provider)
providers_clients_repository = SQLRepository(Companies)
products_repository = SQLRepository(Product)
TransactionHistoryRepository = SQLRepository(TransactionHistory)
transaction_history_files_repository = SQLRepository(TransactionHistoryFile)
product_predictions_repository = SQLRepository(ProductPrediction)

