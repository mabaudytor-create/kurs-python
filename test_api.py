import requests

BASE_URL = "http://127.0.0.1:5000"

# GET – pobierz wszystkie produkty
odpowiedz = requests.get(f"{BASE_URL}/produkty")
print("Wszystkie produkty:", odpowiedz.json())

# GET – pobierz jeden produkt
odpowiedz = requests.get(f"{BASE_URL}/produkty/1")
print("Produkt 1:", odpowiedz.json())

# POST – dodaj nowy produkt
nowy = {"nazwa": "Jajka", "cena": 12.99}
odpowiedz = requests.post(f"{BASE_URL}/produkty", json=nowy)
print("Dodano:", odpowiedz.json())

# PUT – zaktualizuj produkt
aktualizacja = {"cena": 5.00}
odpowiedz = requests.put(f"{BASE_URL}/produkty/1", json=aktualizacja)
print("Zaktualizowano:", odpowiedz.json())

# DELETE – usuń produkt
odpowiedz = requests.delete(f"{BASE_URL}/produkty/2")
print("Usunięto:", odpowiedz.json())

# Sprawdź czy produkt zniknął
odpowiedz = requests.get(f"{BASE_URL}/produkty/2")
print("Status:", odpowiedz.status_code)  # 404
