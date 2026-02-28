import pyodbc

# ==========================
# KONFIGURACJA
# ==========================

SERVER = r"localhost\SQLEXPRESS"   # dostosuj
DATABASE = "StatystykiWWW"
DRIVER = "ODBC Driver 17 for SQL Server"

# ==========================
# POŁĄCZENIE
# ==========================

def get_connection(database="master"):
    return pyodbc.connect(
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )

# ==========================
# INICJALIZACJA BAZY
# ==========================

def init_database():
    conn = get_connection("master")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"""
        IF DB_ID('{DATABASE}') IS NULL
            CREATE DATABASE {DATABASE};
    """)

    cursor.close()
    conn.close()

    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        IF OBJECT_ID('licznik_odwiedzin', 'U') IS NULL
        CREATE TABLE licznik_odwiedzin (
            id INT PRIMARY KEY IDENTITY(1,1),
            nazwa_strony NVARCHAR(200) NOT NULL UNIQUE,
            liczba_odwiedzin BIGINT NOT NULL DEFAULT 0,
            data_aktualizacji DATETIME2 DEFAULT SYSDATETIME()
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()

# ==========================
# LOGIKA BIZNESOWA
# ==========================

def odwiedz_strone(nazwa_strony: str):
    """
    Atomowe zwiększenie licznika odwiedzin.
    """
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        MERGE licznik_odwiedzin AS target
        USING (SELECT ? AS nazwa_strony) AS source
        ON target.nazwa_strony = source.nazwa_strony

        WHEN MATCHED THEN
            UPDATE SET 
                liczba_odwiedzin = liczba_odwiedzin + 1,
                data_aktualizacji = SYSDATETIME()

        WHEN NOT MATCHED THEN
            INSERT (nazwa_strony, liczba_odwiedzin)
            VALUES (source.nazwa_strony, 1);
    """, (nazwa_strony,))

    conn.commit()
    cursor.close()
    conn.close()


def top_strony(n: int):
    """
    Zwraca n najpopularniejszych stron malejąco wg liczby odwiedzin.
    """
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP (?) nazwa_strony, liczba_odwiedzin
        FROM licznik_odwiedzin
        ORDER BY liczba_odwiedzin DESC;
    """, (n,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [(row[0], row[1]) for row in rows]


# ==========================
# TEST
# ==========================

if __name__ == "__main__":
    init_database()

    # symulacja ruchu
    odwiedz_strone("strona_glowna")
    odwiedz_strone("strona_glowna")
    odwiedz_strone("blog")
    odwiedz_strone("kontakt")
    odwiedz_strone("strona_glowna")
    odwiedz_strone("kontakt")

    print("TOP 3 strony:")
    print(top_strony(3))

