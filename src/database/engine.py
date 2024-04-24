# get the environment variables
from os import environ, getcwd, path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to return a new session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Carregar o conteúdo do arquivo SQL
# Obter o diretório atual
current_dir = path.dirname(__file__)

# Concatenar o nome do arquivo ao diretório atual
sql_file_path = path.join(current_dir, 'create_tables.sql')

with open(sql_file_path, 'r') as file:
    sql_content = file.read()

# Executar o conteúdo SQL
with engine.connect() as connection:
    query = text(sql_content)
    result = connection.execute(query)

# Verificar se a execução foi bem-sucedida
if result:
    print("Arquivo SQL executado com sucesso.")
else:
    print("Falha ao executar o arquivo SQL.")
