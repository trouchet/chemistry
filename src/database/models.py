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

class ProviderDB(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)

class CompanyDB(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))
    provider = relationship("ProviderDB", back_populates="companies")

class ClientDB(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship("CompanyDB", back_populates="clients")

class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))
    provider = relationship("ProviderDB", back_populates="products")

class TransactionHistoryDB(Base):
    __tablename__ = "transations_history"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    item_id = Column(Integer, index=True)

class RecommendationDB(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserDB", back_populates="recommendations")
    item_id = Column(Integer, index=True)

# Define relationships
ProviderDB.companies = relationship("CompanyDB", back_populates="provider")
CompanyDB.clients = relationship("ClientDB", back_populates="company")
ProviderDB.products = relationship("ProductDB", back_populates="provider")
UserDB.recommendations = relationship("RecommendationDB", back_populates="user")