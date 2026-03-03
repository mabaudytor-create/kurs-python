import os
import time
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Tymczasowo zmieniamy sposób importu redis, aby zobaczyć, czy to coś zmieni
# Jeśli wcześniej był błąd "No module named 'redis'", to ta linijka będzie miejscem błędu
try:
    import redis
    print("DEBUG: Moduł 'redis' zaimportowany pomyślnie w database.py!")
except ImportError as e:
    print(f"DEBUG: BŁĄD IMPORTU 'redis' w database.py: {e}")
    # Jeśli to się wydarzy, to nadal mamy problem z dostępnością modułu mimo pip freeze
    raise

# ────────────────────────────────────────────────
# USTAWIENIA – zmień tylko jeśli coś się zmieniło
# ────────────────────────────────────────────────

SQL_SERVER = os.getenv("SQL_SERVER", "host.docker.internal")
SQL_PORT = os.getenv("SQL_PORT", "1434")
SQL_INSTANCE_NAME = os.getenv("SQL_INSTANCE_NAME", "SQLEXPRESS2022")
SQL_DB = os.getenv("SQL_DB", "KursPython")
SQL_USER = os.getenv("SQL_USER", "app_user")
SQL_PASS = os.getenv("SQL_PASS", "MAB@mab1707")

# ────────────────────────────────────────────────
# Connection string
# ────────────────────────────────────────────────

DATABASE_URL = (
    f"mssql+pyodbc://{SQL_USER}:{SQL_PASS}@"
    f"/?odbc_connect="
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER}\\{SQL_INSTANCE_NAME},{SQL_PORT};"
    f"DATABASE={SQL_DB};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASS};"
    f"TrustServerCertificate=yes;"
    f"Encrypt=yes;"
    f"ConnectionTimeout=300;" # Wydłużony timeout na poziomie DSN
    f"MultipleActiveResultSets=true;"
)

# ────────────────────────────────────────────────
# Engine i sesja SQLAlchemy - WYŁĄCZONA PULA POŁĄCZEŃ
# ────────────────────────────────────────────────

engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=None,
    pool_pre_ping=False,
    pool_size=0,
    max_overflow=0,
    pool_timeout=0,
    connect_args={
        'timeout': 300, # Wydłużony timeout dla connect_args
        'autocommit': True,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ────────────────────────────────────────────────
# Redis – inicjalizacja
# ────────────────────────────────────────────────

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Tutaj inicjalizujemy instancję r, która jest importowana w main.py
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# ────────────────────────────────────────────────
# Funkcja czekająca na bazę
# ────────────────────────────────────────────────

def wait_for_sqlserver(timeout=180):
    start = time.time()
    attempt = 0

    print("--- ROZPOCZYNAM TEST POŁĄCZENIA Z SQL SERVER ---")

    sql_server_host = os.getenv("SQL_SERVER", "host.docker.internal")
    sql_port = os.getenv("SQL_PORT", "1434")
    sql_instance_name = os.getenv("SQL_INSTANCE_NAME", "SQLEXPRESS2022")
    sql_db = os.getenv("SQL_DB", "KursPython")
    sql_user = os.getenv("SQL_USER", "app_user")
    sql_pass = os.getenv("SQL_PASS", "MAB@mab1707")

    pyodbc_connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={sql_server_host}\\{sql_instance_name},{sql_port};"
        f"DATABASE={sql_db};"
        f"UID={sql_user};"
        f"PWD={sql_pass};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes;"
        f"ConnectionTimeout=10;"
    )

    print(f"Testowy string połączenia pyodbc: {pyodbc_connection_string}")

    while time.time() - start < timeout:
        attempt += 1
        try:
            print(f"Oczekiwanie na SQL (pyodbc)... próba {attempt}")
            with pyodbc.connect(pyodbc_connection_string) as conn_test:
                cursor_test = conn_test.cursor()
                cursor_test.execute("SELECT 1")
                result_test = cursor_test.fetchone()
                print(f"SQL Server jest dostępny poprzez pyodbc! Wynik testu: {result_test[0]} (po {attempt} próbach)")

            try:
                with engine.connect() as conn:
                    print(f"SQL Server jest dostępny przez SQLAlchemy! (po {attempt} próbach)")
                    return True
            except Exception as sa_e:
                print(f"BŁĄD: Połączenie pyodbc udane, ale SQLAlchemy zawiodło! Szczegóły: {str(sa_e)}")
                time.sleep(8)
                continue

        except pyodbc.Error as pyodbc_err:
            print(f"Oczekiwanie na SQL (błąd pyodbc)... próba {attempt} → {str(pyodbc_err)}")
            time.sleep(4)
        except Exception as general_err:
            print(f"Oczekiwanie na SQL (ogólny błąd)... próba {attempt} → {str(general_err)}")
            time.sleep(4)

    raise Exception(f"SQL Server nie jest dostępny po {timeout} sekundach")
