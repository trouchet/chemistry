# get the environment variables
from os import environ

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)

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

# Crie uma sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

