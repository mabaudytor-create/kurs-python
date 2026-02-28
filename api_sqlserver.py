import pyodbc
import redis
import json
import time
from flask import Flask, jsonify

# ========================
# KONFIGURACJA
# ========================

SQL_SERVER = r"localhost\SQLEXPRESS"  # zmień jeśli potrzeba
SQL_DATABASE = "CacheAPI"
SQL_DRIVER = "ODBC Driver 17 for SQL Server"

REDIS_HOST = "localhost"
REDIS_PORT = 6379
CACHE_TTL = 60  # sekundy

app = Flask(__name__)

# ========================
# POŁĄCZENIA
# ========================

def get_sql_connection():
    return pyodbc.connect(
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        "Trusted_Connection=yes;"
    )

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# ========================
# INICJALIZACJA BAZY
# ========================

def init_database():
    conn = pyodbc.connect(
        f"DRIVER={{{SQL_DRIVER}}};"
        f"SERVER={SQL_SERVER};"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        IF DB_ID('CacheAPI') IS NULL
            CREATE DATABASE CacheAPI;
    """)

    cursor.close()
    conn.close()

    conn = get_sql_connection()
    cursor = conn.cursor()

    cursor.execute("""
        IF OBJECT_ID('produkty', 'U') IS NULL
        CREATE TABLE produkty (
            id INT PRIMARY KEY,
            nazwa NVARCHAR(100),
            cena DECIMAL(10,2)
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM produkty")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO produkty VALUES (1, 'Laptop', 4500.00)")
        cursor.execute("INSERT INTO produkty VALUES (2, 'Telefon', 3000.00)")
        cursor.execute("INSERT INTO produkty VALUES (3, 'Monitor', 1200.00)")

    conn.commit()
    cursor.close()
    conn.close()

# ========================
# LOGIKA CACHE (cache-aside)
# ========================

def get_product(product_id):
    cache_key = f"produkt:{product_id}"

    # 1️⃣ Sprawdzenie cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("CACHE HIT")
        return json.loads(cached_data)

    print("CACHE MISS – pobieram z SQL Server")

    # 2️⃣ Pobranie z SQL Server
    conn = get_sql_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nazwa, cena FROM produkty WHERE id = ?",
        (product_id,)
    )
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        result = {
            "id": row[0],
            "nazwa": row[1],
            "cena": float(row[2])
        }

        # 3️⃣ Zapis do Redis z TTL 60 sekund
        redis_client.setex(cache_key, CACHE_TTL, json.dumps(result))
        return result

    return None

# ========================
# API
# ========================

@app.route("/produkt/<int:product_id>")
def produkt(product_id):
    result = get_product(product_id)

    if result:
        return jsonify(result)
    return jsonify({"error": "Nie znaleziono"}), 404


if __name__ == "__main__":
    init_database()
    app.run(debug=True)
