from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# from src.database.engine import engine
# # Create tables if they do not exist
# Base.metadata.create_all(bind=engine)

# Define the database models
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class FornecedorDB(Base):
    __tablename__ = "fornecedores"

    forn_id = Column(Integer, primary_key=True, index=True)


class CompanyDB(Base):
    __tablename__ = "   "

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))
    provider = relationship("ProviderDB", back_populates="companies")


class ClienteDB(Base):
    __tablename__ = "clients"

    clie_id = Column(Integer, primary_key=True, index=True)
    clie_token = Column(String)
    clie_status = Column(String)

class ProdutoDB(Base):
    __tablename__ = "produtos"

    prod_id = Column(Integer, primary_key=True, index=True)
    prod_sku = Column(String, index=True)
    prod_nome = Column(String)
    prod_descricao = Column(String)
    prod_fornecedor = Column(String)    

class ProdutoFotoDB(Base):
    __table__ = "produtos_fotos"


class HistoricoDeVendaDB(Base):
    __tablename__ = "historico_venda"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    item_id = Column(Integer, index=True)


class HistoricoVendaArquivoDB(Base):
    __tablename__ = "historico_venda_arquivo"

    hvar_id = Column(Integer, primary_key=True, index=True)
    hvar_provider_id = Column(Integer, ForeignKey('providers.id'))


class RecomendacaoDB(Base):
    __tablename__ = "recomendacoes"

    reco_id = Column(Integer, primary_key=True, index=True)
    reco_sku = Column(String, index=True)
    reco_cliente = Column(String, index=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserDB", back_populates="recommendations")
    item_id = Column(Integer, index=True)


# Define relationships
FornecedorDB.companies = relationship("CompanyDB", back_populates="provider")
UserDB.recommendations = relationship("RecommendationDB", back_populates="user")
