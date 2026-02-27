import sqlite3

# Połączenie z bazą (tworzy plik jeśli nie istnieje)
conn = sqlite3.connect("moja_baza.db")
cursor = conn.cursor()

# Tworzenie tabeli
cursor.execute("""
    CREATE TABLE IF NOT EXISTS uzytkownicy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imie TEXT NOT NULL,
        nazwisko TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        wiek INTEGER
    )
""")

# Dodawanie danych
cursor.execute("""
    INSERT INTO uzytkownicy (imie, nazwisko, email, wiek)
    VALUES (?, ?, ?, ?)
""", ("Mirek", "Kowalski", "mirek@email.com", 77))

cursor.execute("""
    INSERT INTO uzytkownicy (imie, nazwisko, email, wiek)
    VALUES (?, ?, ?, ?)
""", ("Anna", "Nowak", "anna@email.com", 25))

conn.commit()

# Pobieranie danych
cursor.execute("SELECT * FROM uzytkownicy")
wszyscy = cursor.fetchall()
print("Wszyscy użytkownicy:")
for u in wszyscy:
    print(u)

# Pobieranie jednego rekordu
cursor.execute(
    "SELECT * FROM uzytkownicy WHERE imie = ?",
    ("Mirek",)
)
mirek = cursor.fetchone()
print("\nMirek:", mirek)

# Aktualizacja
cursor.execute(
    "UPDATE uzytkownicy SET wiek = ? WHERE email = ?",
    (78, "mirek@email.com")
)
conn.commit()

# Usuwanie
cursor.execute(
    "DELETE FROM uzytkownicy WHERE email = ?",
    ("anna@email.com",)
)
conn.commit()

# Zamknięcie połączenia
conn.close()
print("\nGotowe!")

# Ćwiczenie 1   - biblioteka  plik: moja_baza.db

import sqlite3
from datetime import datetime

# --- Inicjalizacja bazy danych ---
conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

# Tworzymy tabelę książek
cursor.execute("""
CREATE TABLE IF NOT EXISTS ksiazki (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tytul TEXT NOT NULL,
    autor TEXT NOT NULL,
    rok INTEGER,
    dostepna INTEGER DEFAULT 1
)
""")

# Tworzymy tabelę wypożyczeń
cursor.execute("""
CREATE TABLE IF NOT EXISTS wypozyczenia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ksiazka_id INTEGER NOT NULL,
    czytelnik TEXT NOT NULL,
    data_wypozyczenia TEXT NOT NULL,
    FOREIGN KEY (ksiazka_id) REFERENCES ksiazki(id)
)
""")

conn.commit()

# --- Funkcje operacyjne ---

def dodaj_ksiazke(tytul, autor, rok):
    cursor.execute(
        "INSERT INTO ksiazki (tytul, autor, rok, dostepna) VALUES (?, ?, ?, 1)",
        (tytul, autor, rok)
    )
    conn.commit()
    print(f"Dodano książkę: {tytul} autor: {autor}")

def lista_dostepnych():
    cursor.execute("SELECT id, tytul, autor, rok FROM ksiazki WHERE dostepna = 1")
    ksiazki = cursor.fetchall()
    print("Dostępne książki:")
    for k in ksiazki:
        print(f"{k[0]}. {k[1]} ({k[2]}, {k[3]})")
    return ksiazki

def wypozycz_ksiazke(ksiazka_id, czytelnik):
    cursor.execute("SELECT dostepna FROM ksiazki WHERE id = ?", (ksiazka_id,))
    result = cursor.fetchone()
    if not result:
        print("Nie ma takiej książki w bazie.")
        return
    if result[0] == 0:
        print("Książka jest już wypożyczona.")
        return
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO wypozyczenia (ksiazka_id, czytelnik, data_wypozyczenia) VALUES (?, ?, ?)",
        (ksiazka_id, czytelnik, data)
    )
    cursor.execute("UPDATE ksiazki SET dostepna = 0 WHERE id = ?", (ksiazka_id,))
    conn.commit()
    print(f"Książka id={ksiazka_id} wypożyczona dla {czytelnik}.")

def zwroc_ksiazke(ksiazka_id):
    cursor.execute("SELECT dostepna FROM ksiazki WHERE id = ?", (ksiazka_id,))
    result = cursor.fetchone()
    if not result:
        print("Nie ma takiej książki w bazie.")
        return
    if result[0] == 1:
        print("Książka jest już dostępna w bibliotece.")
        return
    cursor.execute("UPDATE ksiazki SET dostepna = 1 WHERE id = ?", (ksiazka_id,))
    conn.commit()
    print(f"Książka id={ksiazka_id} została zwrócona do biblioteki.")

# --- Przykładowe użycie ---
if __name__ == "__main__":
    dodaj_ksiazke("Lalka", "Bolesław Prus", 1890)
    dodaj_ksiazke("Pan Tadeusz", "Adam Mickiewicz", 1834)

    lista_dostepnych()

    wypozycz_ksiazke(1, "Jan Kowalski")
    lista_dostepnych()

    zwroc_ksiazke(1)
    lista_dostepnych()
