import mysql.connector

# 1️⃣ Połączenie z MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="<MAB1707>"
)
cursor = conn.cursor()

# 2️⃣ Tworzenie bazy danych
cursor.execute("CREATE DATABASE IF NOT EXISTS sklep")
cursor.execute("USE sklep")

# 3️⃣ Tworzenie tabel
cursor.execute("""
CREATE TABLE IF NOT EXISTS klienci (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    email VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS zamowienia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    klient_id INT NOT NULL,
    produkt VARCHAR(100),
    ilosc INT,
    cena DECIMAL(10,2),
    data_zamowienia DATE,
    FOREIGN KEY (klient_id) REFERENCES klienci(id)
)
""")

# 4️⃣ Dodanie przykładowych danych
cursor.execute("INSERT INTO klienci (imie, nazwisko, email) VALUES ('Jan', 'Kowalski', 'jan.kowalski@example.com')")
cursor.execute("INSERT INTO klienci (imie, nazwisko, email) VALUES ('Anna', 'Nowak', 'anna.nowak@example.com')")

cursor.execute("""
INSERT INTO zamowienia (klient_id, produkt, ilosc, cena, data_zamowienia)
VALUES (1, 'Laptop', 1, 3500.00, '2026-02-01')
""")

conn.commit()

# 5️⃣ Zapytania SELECT
cursor.execute("SELECT * FROM klienci")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM zamowienia WHERE klient_id = 1")
for row in cursor.fetchall():
    print(row)

conn.close()
