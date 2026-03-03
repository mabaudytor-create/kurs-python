import os
import pyodbc
import time

print("--- ROZPOCZYNAM TEST POŁĄCZENIA Z SQL SERVER ---")

# Ustawienia połączenia (pobieramy z tych samych zmiennych środowiskowych co aplikacja)
SQL_SERVER_HOST = os.getenv("SQL_SERVER", "host.docker.internal")
SQL_PORT = os.getenv("SQL_PORT", "1434")
SQL_INSTANCE_NAME = os.getenv("SQL_INSTANCE_NAME", "SQLEXPRESS2022")
SQL_DB = os.getenv("SQL_DB", "KursPython")
SQL_USER = os.getenv("SQL_USER", "app_user")
SQL_PASS = os.getenv("SQL_PASS", "MAB@mab1707")

# Przygotowanie connection stringu
# Upewnij się, że nazwa sterownika jest poprawna, tak jak w Twoim database.py
CONNECTION_STRING = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER_HOST}\\{SQL_INSTANCE_NAME},{SQL_PORT};"  # Uwaga: tutaj przecinek po instancji, nie dwukropek!
    f"DATABASE={SQL_DB};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASS};"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
    "ConnectionTimeout=10;"  # Skróć timeout, żeby szybciej dostać błąd
)

print(f"Próba połączenia z: {SQL_SERVER_HOST}\\{SQL_INSTANCE_NAME} na porcie {SQL_PORT}")
print(f"Używając stringu: {CONNECTION_STRING}")

# Próba połączenia
try:
    start_time = time.time()
    conn = pyodbc.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")  # Proste zapytanie testowe
    result = cursor.fetchone()
    conn.close()
    end_time = time.time()
    print(f"SUKCES! Połączono z SQL Server w {end_time - start_time:.2f} sekund.")
    print(f"Wynik zapytania testowego: {result[0]}")
except Exception as e:
    print(f"BŁĄD POŁĄCZENIA Z SQL SERVER: {e}")

print("--- TEST POŁĄCZENIA ZAKOŃCZONY ---")
