# get the environment variables
from os import environ, getcwd, path

from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData
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

# Crie uma instância de MetaData
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crie uma instância de declarative_base
Base: DeclarativeMeta = declarative_base(metadata=metadata)

# Crie uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

