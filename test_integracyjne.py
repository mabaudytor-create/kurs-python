# Testy integracyjne API
# Testy integracyjne sprawdzają czy cały system działa razem
# – nie tylko jedna funkcja ale cały endpoint API

import unittest
from app_db import app, db, Produkt


class TestAPI(unittest.TestCase):

    def setUp(self):
        """Konfiguracja testowej bazy danych."""
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Czyszczenie po każdym teście."""
        with app.app_context():
            db.drop_all()

    def test_pobierz_pusta_liste(self):
        odpowiedz = self.client.get("/produkty")
        self.assertEqual(odpowiedz.status_code, 200)
        self.assertEqual(odpowiedz.get_json(), [])

    def test_dodaj_produkt(self):
        dane = {"nazwa": "Chleb", "cena": 4.50}
        odpowiedz = self.client.post("/produkty", json=dane)
        self.assertEqual(odpowiedz.status_code, 201)
        wynik = odpowiedz.get_json()
        self.assertEqual(wynik["nazwa"], "Chleb")
        self.assertEqual(wynik["cena"], 4.50)

    def test_pobierz_nieistniejacy_produkt(self):
        odpowiedz = self.client.get("/produkty/999")
        self.assertEqual(odpowiedz.status_code, 404)

    def test_pelny_cykl_crud(self):
        """Test pełnego cyklu: dodaj → pobierz → zaktualizuj → usuń."""

        # Dodaj
        odpowiedz = self.client.post(
            "/produkty",
            json={"nazwa": "Mleko", "cena": 3.20}
        )
        id = odpowiedz.get_json()["id"]

        # Pobierz
        odpowiedz = self.client.get(f"/produkty/{id}")
        self.assertEqual(odpowiedz.get_json()["nazwa"], "Mleko")

        # Zaktualizuj
        odpowiedz = self.client.put(
            f"/produkty/{id}",
            json={"cena": 3.50}
        )
        self.assertEqual(odpowiedz.get_json()["cena"], 3.50)

        # Usuń
        odpowiedz = self.client.delete(f"/produkty/{id}")
        self.assertEqual(odpowiedz.status_code, 200)

        # Sprawdź że zniknął
        odpowiedz = self.client.get(f"/produkty/{id}")
        self.assertEqual(odpowiedz.status_code, 404)


if __name__ == "__main__":
    unittest.main()
