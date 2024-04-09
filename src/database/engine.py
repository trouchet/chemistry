from sqlalchemy import create_engine, Column, Integer, String
from databases import Database
from sqlalchemy.orm import sessionmaker

# get the environment variables
from os import environ

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = environ.get("POSTGRES_DB")
POSTGRES_PORT = environ.get("POSTGRES_PORT", 5432)

credentials = f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
db_info = f'postgres:{POSTGRES_PORT}/{POSTGRES_DB}'
DATABASE_URL = f'postgresql://{credentials}@{db_info}'

print(DATABASE_URL)

## Create a database connection
## FIXME: Unable to connect so far connection 
# engine = create_engine(DATABASE_URL)
# 
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)