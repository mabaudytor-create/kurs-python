import pyodbc


# =========================================================
# KONFIGURACJA POŁĄCZENIA
# =========================================================

def polacz():
    """
    Tworzy połączenie z SQL Server.
    Trusted_Connection=yes oznacza uwierzytelnianie Windows
    – nie potrzebujesz hasła jeśli jesteś zalogowany w Windows!
    """
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=kurs_python;"
        "Trusted_Connection=yes;"
    )
    return conn


# =========================================================
# TWORZENIE BAZY I TABEL – POPRAWIONA WERSJA
# =========================================================

def utworz_baze():
    """Tworzy bazę danych i tabele jeśli nie istnieją."""

    # Połączenie BEZ bazy danych z autocommit=True
    # (SQL Server nie pozwala CREATE DATABASE wewnątrz transakcji)
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "Trusted_Connection=yes;",
        autocommit=True  # ← kluczowa poprawka!
    )
    cursor = conn.cursor()

    # Tworzenie bazy danych
    cursor.execute("""
        IF NOT EXISTS (
            SELECT name FROM sys.databases
            WHERE name = 'kurs_python'
        )
        CREATE DATABASE kurs_python
    """)
    conn.close()
    print("✅ Baza danych kurs_python gotowa!")

    # Teraz łączymy się z nową bazą i tworzymy tabele
    conn = polacz()
    cursor = conn.cursor()

    # Tabela pracowników
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sys.tables
            WHERE name = 'pracownicy'
        )
        CREATE TABLE pracownicy (
            id INT IDENTITY(1,1) PRIMARY KEY,
            imie NVARCHAR(50) NOT NULL,
            nazwisko NVARCHAR(50) NOT NULL,
            stanowisko NVARCHAR(100),
            wynagrodzenie DECIMAL(10, 2),
            data_zatrudnienia DATE,
            aktywny BIT DEFAULT 1
        )
    """)

    # Tabela projektów
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sys.tables
            WHERE name = 'projekty'
        )
        CREATE TABLE projekty (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nazwa NVARCHAR(100) NOT NULL,
            budzet DECIMAL(12, 2),
            data_start DATE,
            data_koniec DATE
        )
    """)

    # Tabela łącząca pracowników z projektami (relacja wiele-do-wielu)
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sys.tables
            WHERE name = 'pracownicy_projekty'
        )
        CREATE TABLE pracownicy_projekty (
            pracownik_id INT,
            projekt_id INT,
            rola NVARCHAR(50),
            PRIMARY KEY (pracownik_id, projekt_id),
            FOREIGN KEY (pracownik_id) REFERENCES pracownicy(id),
            FOREIGN KEY (projekt_id) REFERENCES projekty(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tabele gotowe!")


# =========================================================
# OPERACJE CRUD – PRACOWNICY
# =========================================================

def dodaj_pracownika(imie, nazwisko, stanowisko, wynagrodzenie, data):
    """Dodaje nowego pracownika."""
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pracownicy
            (imie, nazwisko, stanowisko, wynagrodzenie, data_zatrudnienia)
            VALUES (?, ?, ?, ?, ?)
        """, (imie, nazwisko, stanowisko, wynagrodzenie, data))
        conn.commit()
        print(f"✅ Dodano pracownika: {imie} {nazwisko}")


def pobierz_pracownikow():
    """Pobiera wszystkich aktywnych pracowników."""
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, imie, nazwisko, stanowisko, wynagrodzenie
            FROM pracownicy
            WHERE aktywny = 1
            ORDER BY nazwisko ASC
        """)
        return cursor.fetchall()


def aktualizuj_wynagrodzenie(pracownik_id, nowe_wynagrodzenie):
    """Aktualizuje wynagrodzenie pracownika."""
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pracownicy
            SET wynagrodzenie = ?
            WHERE id = ?
        """, (nowe_wynagrodzenie, pracownik_id))
        conn.commit()
        print(f"✅ Zaktualizowano wynagrodzenie pracownika {pracownik_id}")


def usun_pracownika(pracownik_id):
    """
    Miękkie usunięcie – ustawia flagę aktywny = 0.
    Dane pozostają w bazie ale pracownik nie pojawia się w wynikach.
    """
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pracownicy
            SET aktywny = 0
            WHERE id = ?
        """, (pracownik_id,))
        conn.commit()
        print(f"✅ Pracownik {pracownik_id} dezaktywowany")


# =========================================================
# ZAAWANSOWANE ZAPYTANIA SQL
# =========================================================

def statystyki_wynagrodzen():
    """Statystyki wynagrodzeń według stanowiska."""
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                stanowisko,
                COUNT(*) AS liczba_pracownikow,
                AVG(wynagrodzenie) AS srednia,
                MIN(wynagrodzenie) AS minimum,
                MAX(wynagrodzenie) AS maksimum,
                SUM(wynagrodzenie) AS suma
            FROM pracownicy
            WHERE aktywny = 1
            GROUP BY stanowisko
            ORDER BY srednia DESC
        """)
        return cursor.fetchall()


def pracownicy_bez_projektow():
    """Znajduje pracowników nieprzypisanych do żadnego projektu."""
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.imie, p.nazwisko, p.stanowisko
            FROM pracownicy p
            LEFT JOIN pracownicy_projekty pp ON p.id = pp.pracownik_id
            WHERE pp.projekt_id IS NULL
            AND p.aktywny = 1
        """)
        return cursor.fetchall()


def projekty_z_pracownikami():
    """Pobiera projekty wraz z listą pracowników."""
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                pr.nazwa AS projekt,
                p.imie + ' ' + p.nazwisko AS pracownik,
                pp.rola
            FROM projekty pr
            JOIN pracownicy_projekty pp ON pr.id = pp.projekt_id
            JOIN pracownicy p ON pp.pracownik_id = p.id
            ORDER BY pr.nazwa, p.nazwisko
        """)
        return cursor.fetchall()


# =========================================================
# TRANSAKCJE
# =========================================================

def przelew_budzetu(z_projektu_id, do_projektu_id, kwota):
    """
    Przenosi budżet między projektami w transakcji.
    Jeśli cokolwiek się nie uda – obie operacje są cofane.
    """
    conn = polacz()
    try:
        cursor = conn.cursor()

        # Sprawdź czy jest wystarczający budżet
        cursor.execute(
            "SELECT budzet FROM projekty WHERE id = ?",
            (z_projektu_id,)
        )
        wynik = cursor.fetchone()
        if not wynik or wynik[0] < kwota:
            raise ValueError("Niewystarczający budżet!")

        # Odejmij z jednego projektu
        cursor.execute("""
            UPDATE projekty
            SET budzet = budzet - ?
            WHERE id = ?
        """, (kwota, z_projektu_id))

        # Dodaj do drugiego projektu
        cursor.execute("""
            UPDATE projekty
            SET budzet = budzet + ?
            WHERE id = ?
        """, (kwota, do_projektu_id))

        conn.commit()
        print(f"✅ Przelano {kwota} zł między projektami")

    except Exception as e:
        conn.rollback()  # cofnij wszystkie zmiany!
        print(f"❌ Błąd transakcji – cofnięto zmiany: {e}")
    finally:
        conn.close()


# =========================================================
# PROGRAM GŁÓWNY
# =========================================================

if __name__ == "__main__":
    # Tworzenie bazy i tabel
    utworz_baze()

    # Dodawanie pracowników
    dodaj_pracownika("Mirek", "Kowalski", "Programista", 8000, "2020-01-15")
    dodaj_pracownika("Anna", "Nowak", "Designer", 7000, "2021-03-20")
    dodaj_pracownika("Piotr", "Wiśniewski", "Manager", 10000, "2019-06-01")
    dodaj_pracownika("Kasia", "Wójcik", "Programista", 8500, "2022-05-10")

    # Wyświetlenie pracowników
    print("\n👥 Wszyscy pracownicy:")
    for p in pobierz_pracownikow():
        print(f"  [{p[0]}] {p[1]} {p[2]} – {p[3]} – {p[4]} zł")

    # Aktualizacja wynagrodzenia
    aktualizuj_wynagrodzenie(1, 8500)

    # Statystyki
    print("\n📊 Statystyki wynagrodzeń:")
    for s in statystyki_wynagrodzen():
        print(f"  {s[0]}: {s[1]} os., "
              f"średnia {float(s[2]):.2f} zł, "
              f"min {s[3]} zł, max {s[4]} zł")

    # Dezaktywacja pracownika
    usun_pracownika(2)
    print("\n👥 Pracownicy po dezaktywacji Anny:")
    for p in pobierz_pracownikow():
        print(f"  {p[1]} {p[2]}")

    # Pracownicy bez projektów
    print("\n👥 Pracownicy bez projektów:")
    for p in pracownicy_bez_projektow():
        print(f"  {p[1]} {p[2]} – {p[3]}")

