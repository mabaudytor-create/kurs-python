import sqlite3
import datetime


def polacz():
    """Tworzy połączenie z bazą danych."""
    conn = sqlite3.connect("kolejka.db")
    return conn


def utworz_tabele():
    """Tworzy tabelę kolejki jeśli nie istnieje."""
    conn = polacz()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kolejka (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zadanie TEXT NOT NULL,
            status TEXT DEFAULT 'oczekuje',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def dodaj_zadanie(zadanie):
    """Dodaje nowe zadanie do kolejki."""
    conn = polacz()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO kolejka (zadanie) VALUES (?)",
        (zadanie,)
    )
    conn.commit()
    conn.close()
    print(f"✅ Dodano zadanie: {zadanie}")


def pobierz_nastepne():
    """Pobiera i przetwarza pierwsze oczekujące zadanie."""
    conn = polacz()
    cursor = conn.cursor()

    # Pobierz pierwsze oczekujące zadanie (FIFO)
    cursor.execute("""
        SELECT id, zadanie FROM kolejka
        WHERE status = 'oczekuje'
        ORDER BY id ASC
        LIMIT 1
    """)
    zadanie = cursor.fetchone()

    if zadanie:
        id_zadania, nazwa = zadanie
        # Zmień status na 'w trakcie'
        cursor.execute(
            "UPDATE kolejka SET status = 'w trakcie' WHERE id = ?",
            (id_zadania,)
        )
        conn.commit()
        conn.close()
        return id_zadania, nazwa

    conn.close()
    return None


def zakoncz_zadanie(id_zadania):
    """Oznacza zadanie jako zakończone."""
    conn = polacz()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE kolejka SET status = 'zakonczone' WHERE id = ?",
        (id_zadania,)
    )
    conn.commit()
    conn.close()
    print(f"✅ Zadanie {id_zadania} zakończone!")


def wyswietl_kolejke():
    """Wyświetla wszystkie zadania w kolejce."""
    conn = polacz()
    cursor = conn.cursor()
    cursor.execute("SELECT id, zadanie, status FROM kolejka ORDER BY id")
    zadania = cursor.fetchall()
    conn.close()

    print("\n📋 Stan kolejki:")
    print("-" * 40)
    for z in zadania:
        print(f"  [{z[0]}] {z[1]} – {z[2]}")
    print("-" * 40)


# Program główny
if __name__ == "__main__":
    utworz_tabele()

    # Dodajemy zadania
    dodaj_zadanie("Wyślij email do klienta")
    dodaj_zadanie("Wygeneruj raport")
    dodaj_zadanie("Zaktualizuj bazę danych")

    wyswietl_kolejke()

    # Przetwarzamy zadania
    print("\n🔄 Przetwarzanie zadań...")
    for _ in range(3):
        wynik = pobierz_nastepne()
        if wynik:
            id_z, nazwa = wynik
            print(f"⚙️  Przetwarzam: {nazwa}")
            zakoncz_zadanie(id_z)

    wyswietl_kolejke()
