from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    recommendations = relationship("RecomendacaoDB", back_populates="user")


class FornecedorDB(Base):
    __tablename__ = "fornecedores"

    forn_id = Column(Integer, primary_key=True, index=True)
    companies = relationship("CompanyDB", back_populates="provider")


class EmpresaDB(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('fornecedores.forn_id'))
    provider = relationship("FornecedorDB", back_populates="companies")


class ClienteDB(Base):
    __tablename__ = "clientes"

    clie_id = Column(Integer, primary_key=True, index=True)
    clie_token = Column(String)
    clie_status = Column(String)


class ProdutosDB(Base):
    __tablename__ = "produtos"

    prod_id = Column(Integer, primary_key=True, index=True)
    prod_sku = Column(String, index=True)
    prod_nome = Column(String)
    prod_descricao = Column(String)
    prod_fornecedor = Column(String)


class ProdutoFotoDB(Base):
    __tablename__ = "produtos_fotos"


class HistoricoDeVendaDB(Base):
    __tablename__ = "historico_venda"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('fornecedores.forn_id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    client_id = Column(Integer, ForeignKey('clients.clie_id'))
    item_id = Column(Integer, index=True)


class HistoricoVendaArquivoDB(Base):
    __tablename__ = "historico_venda_arquivo"

    hvar_id = Column(Integer, primary_key=True, index=True)
    hvar_provider_id = Column(Integer, ForeignKey('fornecedores.forn_id'))


class RecomendacaoDB(Base):
    __tablename__ = "recomendacoes"

    reco_id = Column(Integer, primary_key=True, index=True)
    reco_sku = Column(String, index=True)
    reco_cliente = Column(String, index=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserDB", back_populates="recommendations")
    item_id = Column(Integer, index=True)
