import pyodbc
from datetime import datetime

# ==============================
# KONFIGURACJA POŁĄCZENIA
# ==============================
SERVER = "localhost"
DATABASE_MASTER = "master"
DATABASE_NAME = "Biblioteka"

CONNECTION_STRING_MASTER = f"""
DRIVER={{ODBC Driver 17 for SQL Server}};
SERVER={SERVER};
DATABASE={DATABASE_MASTER};
Trusted_Connection=yes;
"""

CONNECTION_STRING_DB = f"""
DRIVER={{ODBC Driver 17 for SQL Server}};
SERVER={SERVER};
DATABASE={DATABASE_NAME};
Trusted_Connection=yes;
"""


# ==============================
# TWORZENIE BAZY I TABEL
# ==============================
def inicjalizacja():
    # Tworzenie bazy jeśli nie istnieje
    with pyodbc.connect(CONNECTION_STRING_MASTER, autocommit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{DATABASE_NAME}')
        CREATE DATABASE {DATABASE_NAME}
        """)

    # Tworzenie tabel
    with pyodbc.connect(CONNECTION_STRING_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ksiazki' AND xtype='U')
        CREATE TABLE ksiazki (
            id INT PRIMARY KEY IDENTITY(1,1),
            tytul NVARCHAR(200) NOT NULL,
            autor NVARCHAR(200) NOT NULL,
            rok INT,
            dostepna BIT DEFAULT 1
        )
        """)

        cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='wypozyczenia' AND xtype='U')
        CREATE TABLE wypozyczenia (
            id INT PRIMARY KEY IDENTITY(1,1),
            ksiazka_id INT FOREIGN KEY REFERENCES ksiazki(id),
            czytelnik NVARCHAR(200),
            data_wypozyczenia DATETIME
        )
        """)

        conn.commit()


# ==============================
# FUNKCJE OPERACYJNE
# ==============================

def dodaj_ksiazke(tytul, autor, rok):
    with pyodbc.connect(CONNECTION_STRING_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO ksiazki (tytul, autor, rok)
        VALUES (?, ?, ?)
        """, (tytul, autor, rok))
        conn.commit()
        print("Dodano książkę.")


def wypozycz_ksiazke(ksiazka_id, czytelnik):
    with pyodbc.connect(CONNECTION_STRING_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT dostepna FROM ksiazki WHERE id = ?", (ksiazka_id,))
        row = cursor.fetchone()

        if not row:
            print("Nie istnieje taka książka.")
            return

        if not row[0]:
            print("Książka jest już wypożyczona.")
            return

        cursor.execute("""
        INSERT INTO wypozyczenia (ksiazka_id, czytelnik, data_wypozyczenia)
        VALUES (?, ?, ?)
        """, (ksiazka_id, czytelnik, datetime.now()))

        cursor.execute("""
        UPDATE ksiazki SET dostepna = 0 WHERE id = ?
        """, (ksiazka_id,))

        conn.commit()
        print("Wypożyczono książkę.")


def zwroc_ksiazke(ksiazka_id):
    with pyodbc.connect(CONNECTION_STRING_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE ksiazki SET dostepna = 1 WHERE id = ?
        """, (ksiazka_id,))

        conn.commit()
        print("Książka została zwrócona.")


def lista_dostepnych():
    with pyodbc.connect(CONNECTION_STRING_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, tytul, autor, rok
        FROM ksiazki
        WHERE dostepna = 1
        """)

        books = cursor.fetchall()

        if not books:
            print("Brak dostępnych książek.")
            return

        print("Dostępne książki:")
        for book in books:
            print(f"ID: {book[0]} | {book[1]} - {book[2]} ({book[3]})")


# ==============================
# URUCHOMIENIE
# ==============================
if __name__ == "__main__":
    inicjalizacja()

    # Przykładowe użycie:
    dodaj_ksiazke("Władca Pierścieni", "J.R.R. Tolkien", 1954)
    dodaj_ksiazke("1984", "George Orwell", 1949)

    lista_dostepnych()

    wypozycz_ksiazke(1, "Jan Kowalski")
    lista_dostepnych()

    zwroc_ksiazke(1)
    lista_dostepnych()

