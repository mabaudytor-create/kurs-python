from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import redis
import time

# Pobranie zmiennych środowiskowych z docker-compose
SQL_SERVER = os.getenv("SQL_SERVER", "localhost")
SQL_DB = os.getenv("SQL_DB", "Sklep")
SQL_USER = os.getenv("SQL_USER", "sa")
SQL_PASS = os.getenv("SQL_PASS", "YourStrong@Passw0rd")

# Połączenie z SQL Server (ODBC)
DATABASE_URL = f"mssql+pyodbc://{SQL_USER}:{SQL_PASS}@{SQL_SERVER}/{SQL_DB}?driver=ODBC+Driver+18+for+SQL+Server"

# SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Połączenie z Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Prosta funkcja czekająca aż SQL Server będzie dostępny
def wait_for_sqlserver(timeout=30):
    start = time.time()
    while True:
        try:
            with engine.connect() as conn:
                return True
        except Exception:
            if time.time() - start > timeout:
                raise Exception("SQL Server nie jest dostępny")
            time.sleep(1)

