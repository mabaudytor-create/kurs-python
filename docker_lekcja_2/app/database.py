from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import redis
import time

# Pobranie zmiennych środowiskowych z docker-compose
SQL_SERVER = os.getenv("SQL_SERVER", "host.docker.internal")
SQL_PORT   = os.getenv("SQL_PORT", "1433")
SQL_DB     = os.getenv("SQL_DB", "KursPython")
SQL_USER   = os.getenv("SQL_USER", "sa")
SQL_PASS   = os.getenv("SQL_PASS", "YourStrong@Passw0rd")  # ← zmień na prawdziwe hasło

# Connection string – wersja z IP + portem (bez nazwy instancji)
DATABASE_URL = (
    f"mssql+pyodbc://{SQL_USER}:{SQL_PASS}@{SQL_SERVER}:{SQL_PORT}/{SQL_DB}"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&TrustServerCertificate=yes"
    "&Encrypt=no"
    "&ConnectionTimeout=45"
)

# Engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True → pokazuje wszystkie zapytania w logach

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis – bez zmian
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Funkcja sprawdzająca dostępność bazy – dłuższy timeout i wolniejsze próby
def wait_for_sqlserver(timeout=180):
    start = time.time()
    attempt = 0

    while time.time() - start < timeout:
        attempt += 1
        try:
            with engine.connect() as conn:
                print(f"SQL Server jest dostępny! (po {attempt} próbach)")
                return True
        except Exception as e:
            print(f"Oczekiwanie na SQL... próba {attempt} → {str(e)}")
            time.sleep(5)  # 5 sekund przerwy – mniej spamu w logach

    raise Exception(f"SQL Server nie jest dostępny po {timeout} sekundach")
