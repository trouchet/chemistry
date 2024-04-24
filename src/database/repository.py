from abc import ABC, abstractmethod
from typing import List, TypeVar

from sqlalchemy.orm import Session
from src.database.models import (
        Usuarios, \
        Fornecedores, \
        Clientes, \
        Produtos, \
        HistoricoVenda, \
        HistoricoVendaArquivo, \
        Recomendacoes
    )

T = TypeVar('T')

class BaseRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> T:
        pass

    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        pass

def create_repository(model_cls):
    class Repository(BaseRepository):
        def __init__(self, db: Session):
            self.db = db

        def find_all(self) -> List[model_cls]:
            return self.db.query(model_cls).all()

        def save(self, entity: model_cls) -> model_cls:
            if entity.id:
                self.db.merge(entity)
            else:
                self.db.add(entity)
            self.db.commit()
            return entity

        def find_by_id(self, id: int) -> model_cls:
            return self.db.query(model_cls).filter(model_cls.id == id).first()

        def exists_by_id(self, id: int) -> bool:
            return self.db.query(model_cls).filter(model_cls.id == id).first() is not None

        def delete_by_id(self, id: int) -> None:
            entity = self.db.query(model_cls).filter(model_cls.id == id).first()
            if entity is not None:
                self.db.delete(entity)
                self.db.commit()

    return Repository

RepositorioUsuarios = create_repository(Usuarios)
RepositorioFornecedores = create_repository(Fornecedores)
RepositorioClientes = create_repository(Clientes)
RepositorioProdutos = create_repository(Produtos)
RepositorioHistoricoVenda = create_repository(HistoricoVenda)
RepositorioHistoricoVendaArquivo = create_repository(HistoricoVendaArquivo)
RepositorioRecomendacoes = create_repository(Recomendacoes)