import os
from dotenv import load_dotenv # type: ignore 
from sqlalchemy import create_engine, text # type: ignore

load_dotenv()

DB_USER = os.getenv('POSTGRES_USER')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_NAME = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT','5432')

ENGINE = create_engine(
    f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
)

def execute_sql(sql: str):
    with ENGINE.begin() as conn:
        conn.execute(text(sql))