import requests
from faker import Faker

API_URL = "http://127.0.0.1:8000"
fake = Faker("pl_PL")

# -------------------------------------------------
# 1️⃣ Logowanie – pobranie tokena JWT
# -------------------------------------------------

login_response = requests.post(
    f"{API_URL}/login",
    data={
        "username": "admin",
        "password": "admin123"
    }
)

if login_response.status_code != 200:
    raise Exception("Błąd logowania")

token = login_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# -------------------------------------------------
# 2️⃣ Generowanie i dodawanie 10 zadań
# -------------------------------------------------

for i in range(10):
    payload = {
        "tytul": fake.sentence(nb_words=4),
        "opis": fake.text(max_nb_chars=120),
        "status": "oczekuje"
    }

    response = requests.post(
        f"{API_URL}/zadania",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        print(f"[OK] Dodano zadanie {i+1}")
    else:
        print(f"[BŁĄD] {response.status_code} – {response.text}")

