import pyodbc


SERVER = r"localhost\SQLEXPRESS"   # dostosuj do swojej instancji
DATABASE = "SklepInternetowy"
DRIVER = "ODBC Driver 17 for SQL Server"


def get_connection(database="master"):
    return pyodbc.connect(
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )


def utworz_baze():
    conn = get_connection("master")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"""
        IF DB_ID('{DATABASE}') IS NULL
            CREATE DATABASE {DATABASE};
    """)

    cursor.close()
    conn.close()


def utworz_tabele():
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        IF OBJECT_ID('klienci', 'U') IS NULL
        CREATE TABLE klienci (
            id INT PRIMARY KEY IDENTITY(1,1),
            imie NVARCHAR(100) NOT NULL,
            email NVARCHAR(150) NOT NULL UNIQUE,
            data_rejestracji DATETIME DEFAULT GETDATE()
        );
    """)

    cursor.execute("""
        IF OBJECT_ID('zamowienia', 'U') IS NULL
        CREATE TABLE zamowienia (
            id INT PRIMARY KEY IDENTITY(1,1),
            klient_id INT NOT NULL,
            data_zamowienia DATETIME DEFAULT GETDATE(),
            wartosc DECIMAL(12,2) NOT NULL,
            FOREIGN KEY (klient_id) REFERENCES klienci(id)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()


def dodaj_dane_przykladowe():
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO klienci (imie, email) VALUES (?, ?)", ("Jan Kowalski", "jan@example.com"))
    cursor.execute("INSERT INTO klienci (imie, email) VALUES (?, ?)", ("Anna Nowak", "anna@example.com"))

    cursor.execute("INSERT INTO zamowienia (klient_id, wartosc) VALUES (?, ?)", (1, 250.00))
    cursor.execute("INSERT INTO zamowienia (klient_id, wartosc) VALUES (?, ?)", (1, 150.50))
    cursor.execute("INSERT INTO zamowienia (klient_id, wartosc) VALUES (?, ?)", (2, 300.00))

    conn.commit()
    cursor.close()
    conn.close()


def wszyscy_klienci():
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, imie, email, data_rejestracji FROM klienci;")
    rows = cursor.fetchall()

    print("\nWSZYSCY KLIENCI:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def zamowienia_klienta(klient_id):
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT z.id, z.data_zamowienia, z.wartosc
        FROM zamowienia z
        WHERE z.klient_id = ?;
    """, (klient_id,))

    rows = cursor.fetchall()

    print(f"\nZAMÓWIENIA KLIENTA ID={klient_id}:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def laczna_wartosc_zamowien():
    conn = get_connection(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT k.id, k.imie, SUM(z.wartosc) AS laczna_wartosc
        FROM klienci k
        LEFT JOIN zamowienia z ON k.id = z.klient_id
        GROUP BY k.id, k.imie;
    """)

    rows = cursor.fetchall()

    print("\nŁĄCZNA WARTOŚĆ ZAMÓWIEŃ KAŻDEGO KLIENTA:")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    utworz_baze()
    utworz_tabele()
    dodaj_dane_przykladowe()

    wszyscy_klienci()
    zamowienia_klienta(1)
    laczna_wartosc_zamowien()

