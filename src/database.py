from sqlalchemy import create_engine
from databases import Database

# get the environment variables
from os import environ

POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT = environ.get("POSTGRES_PORT")
POSTGRES_DB = environ.get("POSTGRES_DB")

credentials = f'${POSTGRES_USER}:${POSTGRES_PASSWORD}'
db_info = f'postgres:${POSTGRES_PORT}/${POSTGRES_DB}'

DATABASE_URL = f'postgres://{credentials}@{db_info}'

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)