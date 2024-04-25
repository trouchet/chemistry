# get the environment variables
from os import environ

from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta

load_dotenv()

POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)

credentials = f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
db_info = f'postgres:{POSTGRES_PORT}/{POSTGRES_DB}'
DATABASE_URL = f'postgresql://{credentials}@{db_info}'

database_url = URL.create(
    drivername="postgresql",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    port=POSTGRES_PORT
)

# Cria uma instância de engine do banco de dados
engine = create_engine(database_url)

# Crie uma instância de MetaData
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crie uma função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crie uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

