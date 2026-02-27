import mysql.connector

# Połączenie z MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="<MAB1707>",  # hasło które ustawiłeś podczas instalacji
)
cursor = conn.cursor()

# Tworzenie bazy danych
cursor.execute("CREATE DATABASE IF NOT EXISTS kurs_python")
cursor.execute("USE kurs_python")

# Tworzenie tabeli
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pracownicy (
        id INT AUTO_INCREMENT PRIMARY KEY,
        imie VARCHAR(50) NOT NULL,
        nazwisko VARCHAR(50) NOT NULL,
        stanowisko VARCHAR(100),
        wynagrodzenie DECIMAL(10, 2),
        data_zatrudnienia DATE
    )
""")

# Dodawanie danych
pracownicy = [
    ("Jan", "Kowalski", "Programista", 8000.00, "2020-01-15"),
    ("Anna", "Nowak", "Designer", 7000.00, "2021-03-20"),
    ("Piotr", "Wiśniewski", "Manager", 10000.00, "2019-06-01"),
]

cursor.executemany("""
    INSERT INTO pracownicy
    (imie, nazwisko, stanowisko, wynagrodzenie, data_zatrudnienia)
    VALUES (%s, %s, %s, %s, %s)
""", pracownicy)

conn.commit()

# Pobieranie danych
cursor.execute("SELECT * FROM pracownicy")
print("Wszyscy pracownicy:")
for p in cursor.fetchall():
    print(p)

# Filtrowanie
cursor.execute(
    "SELECT * FROM pracownicy WHERE wynagrodzenie > %s",
    (7500,)
)
print("\nPracownicy z wynagrodzeniem > 7500:")
for p in cursor.fetchall():
    print(p)

# Agregacja
cursor.execute("""
    SELECT
        stanowisko,
        COUNT(*) as liczba,
        AVG(wynagrodzenie) as srednia
    FROM pracownicy
    GROUP BY stanowisko
""")
print("\nStatystyki:")
for s in cursor.fetchall():
    print(s)

conn.close()

