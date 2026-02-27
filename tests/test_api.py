import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import aplikacji i modeli
from egzamin_8 import app, Base, Zadanie, get_db


# -------------------------------------------------
# KONFIGURACJA WSPÓŁDZIELONEJ BAZY SQLite
# -------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # kluczowe dla SQLite in-memory
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Tworzenie tabel w tej samej instancji połączenia
Base.metadata.create_all(bind=engine)


# -------------------------------------------------
# Dependency override
# -------------------------------------------------

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# -------------------------------------------------
# Fixture czyszczący bazę po każdym teście
# -------------------------------------------------

@pytest.fixture(autouse=True)
def clear_db():
    yield
    db = TestingSessionLocal()
    db.query(Zadanie).delete()
    db.commit()
    db.close()


# -------------------------------------------------
# TESTY CRUD
# -------------------------------------------------

def test_create_zadanie():
    response = client.post(
        "/zadania",
        json={"tytul": "Test zadanie", "opis": "Opis zadania"},
    )
    assert response.status_code in (200, 201)

    data = response.json()
    assert data["tytul"] == "Test zadanie"
    assert data["opis"] == "Opis zadania"
    assert data["status"] == "oczekuje"
    assert "id" in data


def test_create_zadanie_brak_tytulu():
    response = client.post("/zadania", json={"opis": "Bez tytułu"})
    assert response.status_code == 422  # walidacja Pydantic


def test_read_zadania():
    client.post("/zadania", json={"tytul": "Z1"})
    client.post("/zadania", json={"tytul": "Z2"})

    response = client.get("/zadania")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert any(z["tytul"] == "Z1" for z in data)
    assert any(z["tytul"] == "Z2" for z in data)


def test_update_zadanie():
    res = client.post("/zadania", json={"tytul": "Stare"})
    zadanie_id = res.json()["id"]

    response = client.put(
        f"/zadania/{zadanie_id}",
        json={"tytul": "Nowe", "status": "zakończone"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["tytul"] == "Nowe"
    assert data["status"] == "zakończone"


def test_update_zadanie_brak():
    response = client.put("/zadania/9999", json={"tytul": "Nieistniejące"})
    assert response.status_code == 404


def test_delete_zadanie():
    res = client.post("/zadania", json={"tytul": "Do usunięcia"})
    zadanie_id = res.json()["id"]

    response = client.delete(f"/zadania/{zadanie_id}")
    assert response.status_code == 200
    assert "komunikat" in response.json()

    # Próba ponownego usunięcia
    response = client.delete(f"/zadanie/{zadanie_id}")
    assert response.status_code == 404
