# Napisz program który symuluje kolejkę w przychodni.
# Pacjenci mają imię i priorytet (1=pilny, 2=zwykły).
# Użyj heapq żeby obsługiwać pilnych pacjentów przed zwykłymi.

import heapq

class Pacjent:
    def __init__(self, imie, priorytet):
        self.imie = imie
        self.priorytet = priorytet   # 1 = pilny, 2 = zwykły

    def __repr__(self):
        return f"{self.imie} (priorytet: {self.priorytet})"


class KolejkaPrzychodni:
    def __init__(self):
        self._kolejka = []
        self._licznik = 0  # zapewnia kolejność przy tym samym priorytecie

    def dodaj_pacjenta(self, pacjent):
        # (priorytet, licznik, obiekt)
        heapq.heappush(self._kolejka, (pacjent.priorytet, self._licznik, pacjent))
        self._licznik += 1

    def przyjmij_pacjenta(self):
        if not self._kolejka:
            return None
        _, _, pacjent = heapq.heappop(self._kolejka)
        return pacjent

    def czy_pusta(self):
        return len(self._kolejka) == 0


# --- Symulacja działania ---

kolejka = KolejkaPrzychodni()

kolejka.dodaj_pacjenta(Pacjent("Jan", 2))
kolejka.dodaj_pacjenta(Pacjent("Anna", 1))
kolejka.dodaj_pacjenta(Pacjent("Piotr", 2))
kolejka.dodaj_pacjenta(Pacjent("Maria", 1))

print("Przyjmowanie pacjentów:")

while not kolejka.czy_pusta():
    pacjent = kolejka.przyjmij_pacjenta()
    print("Przyjęto:", pacjent)



# Rozbuduj program z SQLite – dodaj funkcję anuluj_zadanie(id)
# która zmienia status na "anulowane" oraz funkcję statystyki()
# która wyświetla ile zadań jest w każdym statusie
# (oczekuje/w trakcie/zakończone/anulowane).

import sqlite3

DB_NAME = "zadania.db"


def polacz():
    return sqlite3.connect(DB_NAME)


def utworz_tabele():
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zadania (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nazwa TEXT NOT NULL,
                priorytet INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'oczekuje'
            )
        """)
        conn.commit()


def dodaj_zadanie(nazwa, priorytet):
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO zadania (nazwa, priorytet, status)
            VALUES (?, ?, 'oczekuje')
        """, (nazwa, priorytet))
        conn.commit()
        print(f"Dodano zadanie: {nazwa}")


def rozpocznij_zadanie(id):
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE zadania
            SET status = 'w trakcie'
            WHERE id = ? AND status = 'oczekuje'
        """, (id,))
        conn.commit()


def zakoncz_zadanie(id):
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE zadania
            SET status = 'zakończone'
            WHERE id = ? AND status = 'w trakcie'
        """, (id,))
        conn.commit()


def anuluj_zadanie(id):
    """
    Zmienia status zadania na 'anulowane'.
    Można anulować zadanie, które nie jest jeszcze zakończone.
    """
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE zadania
            SET status = 'anulowane'
            WHERE id = ? AND status != 'zakończone'
        """, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            print("Nie można anulować – zadanie nie istnieje lub jest zakończone.")
        else:
            print(f"Zadanie {id} zostało anulowane.")


def statystyki():
    """
    Wyświetla liczbę zadań w podziale na status.
    """
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, COUNT(*)
            FROM zadania
            GROUP BY status
        """)
        wyniki = cursor.fetchall()

        print("\n=== Statystyki zadań ===")

        # Inicjalizacja pełnego zestawu statusów
        statusy = {
            "oczekuje": 0,
            "w trakcie": 0,
            "zakończone": 0,
            "anulowane": 0
        }

        for status, liczba in wyniki:
            statusy[status] = liczba

        for status, liczba in statusy.items():
            print(f"{status}: {liczba}")

        print("========================\n")


def pokaz_zadania():
    with polacz() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nazwa, priorytet, status
            FROM zadania
            ORDER BY priorytet ASC, id ASC
        """)
        for row in cursor.fetchall():
            print(row)


if __name__ == "__main__":
    utworz_tabele()

    # Przykładowe dane
    dodaj_zadanie("Zadanie A", 1)
    dodaj_zadanie("Zadanie B", 2)
    dodaj_zadanie("Zadanie C", 1)

    pokaz_zadania()

    rozpocznij_zadanie(1)
    zakoncz_zadanie(1)
    anuluj_zadanie(2)

    pokaz_zadania()
    statystyki()

