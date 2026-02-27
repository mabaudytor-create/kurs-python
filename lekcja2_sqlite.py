import sqlite3


def utworz_baze():
    with sqlite3.connect("sklep.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produkty (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nazwa TEXT NOT NULL,
                cena REAL NOT NULL,
                ilosc INTEGER DEFAULT 0
            )
        """)
        conn.commit()


def dodaj_produkt(nazwa, cena, ilosc):
    with sqlite3.connect("sklep.db") as conn:
        conn.execute(
            "INSERT INTO produkty (nazwa, cena, ilosc) VALUES (?, ?, ?)",
            (nazwa, cena, ilosc)
        )
        conn.commit()


def pobierz_produkty():
    with sqlite3.connect("sklep.db") as conn:
        # row_factory pozwala odczytywać kolumny po nazwie!
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM produkty")
        return [dict(row) for row in cursor.fetchall()]


def znajdz_tanie(max_cena):
    with sqlite3.connect("sklep.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM produkty WHERE cena <= ? ORDER BY cena ASC",
            (max_cena,)
        )
        return [dict(row) for row in cursor.fetchall()]


if __name__ == "__main__":
    utworz_baze()
    dodaj_produkt("Chleb", 4.50, 100)
    dodaj_produkt("Mleko", 3.20, 50)
    dodaj_produkt("Masło", 7.80, 30)
    dodaj_produkt("Kawior", 150.00, 5)

    print("Wszystkie produkty:")
    for p in pobierz_produkty():
        print(p)

    print("\nProdukty do 10 zł:")
    for p in znajdz_tanie(10.0):
        print(p)
