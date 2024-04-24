# get the environment variables
from os import environ, getcwd, path

from dotenv import load_dotenv

from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta

load_dotenv()
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)

credentials = f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
db_info = f'postgres:{POSTGRES_PORT}/{POSTGRES_DB}'
DATABASE_URL = f'postgresql://{credentials}@{db_info}'


## Create a database connection
engine = create_engine(DATABASE_URL)

# Create tables in the database
Base.metadata.create_all(engine)

# Crie uma instância de MetaData
metadata = MetaData()

# Crie uma instância de declarative_base
Base: DeclarativeMeta = declarative_base(metadata=metadata)

# Crie uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Crie o banco de dados e as tabelas
Base.metadata.create_all(bind=engine)

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    Decimal,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class TabelaUsuarios(Base):
    __tablename__ = "usuarios"

    user_id = Column(Integer, primary_key=True, index=True)
    user_signup_timestamp = Column(DateTime)
    user_token_str = Column(String)
    

class TabelaFornecedores(Base):
    __tablename__ = "fornecedores"

    forn_id = Column(Integer, primary_key=True, index=True)
    forn_companies = relationship("EmpresaDB", back_populates="fornecedores")


class TabelaEmpresas(Base):
    __tablename__ = "empresas"

    empr_id = Column(Integer, primary_key=True, index=True)
    empr_provider_id = Column(Integer, ForeignKey('fornecedores.forn_id'))
    empr_fornecedor = relationship("FornecedorDB", back_populates="empresas")


class TabelaClientes(Base):
    __tablename__ = "clientes"

    clie_id = Column(Integer, primary_key=True, index=True)
    clie_token = Column(String)
    clie_status = Column(String)


class TabelaProdutos(Base):
    __tablename__ = "produtos"

    prod_id = Column(Integer, primary_key=True, index=True)
    prod_sku = Column(String, index=True)
    prod_nome = Column(String)
    prod_descricao = Column(String)
    prod_fornecedor = Column(String)


class TabelaProdutosFotos(Base):
    __tablename__ = "produtos_fotos"


class TabelaHistoricoVenda(Base):
    __tablename__ = "historico_venda"

    hive_id = Column(Integer, primary_key=True, nullable=False, index=True)
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


class TabelaHistoricoVendaArquivo(Base):
    __tablename__ = "historico_venda_arquivo"

    hvar_id = Column(Integer, primary_key=True, nullable=False, index=True)
    hvar_erp = Column(Text, nullable=False)
    hvar_erp_cliente_id = Column(Text, nullable=False)
    hvar_nome_arquivo = Column(Text, nullable=False)
    hvar_url = Column(Text, nullable=False)
    hvar_data_envio = Column(DateTime, nullable=False)
    hvar_status = Column(Text, nullable=False)
    hvar_tamanho = Column(Decimal, nullable=False)

class ArquivoRecomendacoes(Base):
    __tablename__ = "recomendacoes"

    reco_id = Column(Integer, primary_key=True, nullable=False, index=True)
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

# Encerre a sessão após o uso
session.close()

