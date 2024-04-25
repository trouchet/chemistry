from typing import Annotated
from fastapi import Depends

from database import models as db_models
from database.base.repository import DatabaseRepository
from src.api.dependencies import get_repository

def create_repository(model):
    return Annotated[
        DatabaseRepository[model],
        Depends(get_repository(model)),
    ]

# Repositórios
UsuariosRepository = create_repository(db_models.Usuarios)
FornecedoresRepository = create_repository(db_models.Fornecedores)
FornecedoresRepository = create_repository(db_models.Fornecedores)
RepositorioClientes = create_repository(db_models.Clientes)
RepositorioProdutos = create_repository(db_models.Produtos)
RepositorioHistoricoVenda = create_repository(db_models.HistoricoVenda)
RepositorioHistoricoVendaArquivo = create_repository(db_models.HistoricoVendaArquivo)
RepositorioRecomendacoes = create_repository(db_models.Recomendacoes)