from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Decimal,
    JSON,
    ForeignKey,
)
import uuid
from sqlalchemy import Column, ForeignKey, orm

from database.engine import Base

PRIMARY_KEY_TYPE = uuid.UUID

class Base(orm.DeclarativeBase):
    """Base database model."""

    pk: orm.Mapped[PRIMARY_KEY_TYPE] = orm.mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

class Usuarios(Base):
    __tablename__ = "usuarios"

    user_id = Column(PRIMARY_KEY_TYPE, primary_key=True, index=True)
    user_signup_timestamp = Column(DateTime)
    user_token_str = Column(String)


class Fornecedores(Base):
    __tablename__ = "fornecedores"

    forn_id = Column(PRIMARY_KEY_TYPE, primary_key=True, index=True)
    forn_companies = relationship("EmpresaDB", back_populates="fornecedores")


class Empresas(Base):
    __tablename__ = "empresas"

    empr_id = Column(PRIMARY_KEY_TYPE, primary_key=True, index=True)
    empr_provider_id = Column(Integer, ForeignKey('fornecedores.forn_id'))
    empr_fornecedor = relationship("FornecedorDB", back_populates="empresas")


class Clientes(Base):
    __tablename__ = "clientes"

    clie_id = Column(PRIMARY_KEY_TYPE, primary_key=True, index=True)
    clie_token = Column(String)
    clie_status = Column(String)


class Produtos(Base):
    __tablename__ = "produtos"

    prod_id = Column(PRIMARY_KEY_TYPE, primary_key=True, index=True)
    prod_sku = Column(String, index=True)
    prod_nome = Column(String)
    prod_descricao = Column(String)
    prod_fornecedor = Column(String)
    prod_categoria = Column(String)


class HistoricoVenda(Base):
    __tablename__ = "historico_venda"

    hive_id = Column(PRIMARY_KEY_TYPE, primary_key=True, nullable=False, index=True)
    hive_transacao_id = Column(Text, nullable=False)
    hive_consumidor = Column(Text, nullable=False)
    hive_sku = Column(Text, nullable=False)
    hive_data_venda = Column(DateTime, nullable=False)
    hive_datahora_inclusao = Column(DateTime)
    hive_ordem = Column(Integer)
    hive_valor = Column(Decimal)
    hive_quantidade = Column(Decimal)
    hive_fornecedor = Column(Text, nullable=False)
    hive_data_processamento = Column(DateTime)
    hive_sku_categoria = Column(Text)
    hive_status = Column(Text, nullable=False)
    hive_erp_cliente_id = Column(Text, nullable=False)
    hive_erp = Column(Text, nullable=False)


class HistoricoVendaArquivo(Base):
    __tablename__ = "historico_venda_arquivo"

    hvar_id = Column(PRIMARY_KEY_TYPE, primary_key=True, nullable=False, index=True)
    hvar_erp = Column(Text, nullable=False)
    hvar_erp_cliente_id = Column(Text, nullable=False)
    hvar_nome_arquivo = Column(Text, nullable=False)
    hvar_url = Column(Text, nullable=False)
    hvar_data_envio = Column(DateTime, nullable=False)
    hvar_status = Column(Text, nullable=False)
    hvar_tamanho = Column(Decimal, nullable=False)
    

class Recomendacoes(Base):
    __tablename__ = "recomendacoes"

    reco_id = Column(PRIMARY_KEY_TYPE, primary_key=True, nullable=False, index=True)
    reco_erp = Column(Text, nullable=False)
    reco_erp_cliente_id = Column(Text, nullable=False)
    reco_consumidor = Column(Text)
    reco_fornecedor = Column(Text)
    reco_sku = Column(Text, nullable=False)
    reco_hash_sku = Column(Text, nullable=False)
    reco_data_processamento = Column(DateTime, nullable=False)
    reco_recomendacao_json = Column(JSON, nullable=False)
    reco_recomendacao_tipo = Column(Text, nullable=False)
    reco_recomendacao_threshold = Column(Integer)
    reco_forecast_quantidade = Column(JSON)
    reco_forecast_ticket_medio = Column(JSON)
    reco_forecast_proxima_compra = Column(JSON)
