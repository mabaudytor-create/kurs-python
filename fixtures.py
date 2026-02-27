# Generowanie danych testowych (fixtures)
# W testach potrzebujemy danych testowych.
# Fixtures to gotowe zestawy danych do testów.

from faker import Faker

fake = Faker("pl_PL")  # polskie dane!


def generuj_uzytkownika():
    """Generuje jednego losowego użytkownika."""
    return {
        "imie": fake.first_name(),
        "nazwisko": fake.last_name(),
        "email": fake.email(),
        "miasto": fake.city(),
        "pesel": fake.pesel(),
        "telefon": fake.phone_number()
    }


def generuj_uzytkownikow(ile):
    """Generuje listę losowych użytkowników."""
    return [generuj_uzytkownika() for _ in range(ile)]


def generuj_produkt():
    """Generuje losowy produkt."""
    return {
        "nazwa": fake.word(),
        "cena": round(fake.pyfloat(min_value=1, max_value=1000), 2),
        "kategoria": fake.random_element(["elektronika", "odzież", "żywność"])
    }


# Generowanie danych
if __name__ == "__main__":
    print("=== Użytkownicy testowi ===")
    for u in generuj_uzytkownikow(3):
        print(u)

    print("\n=== Produkty testowe ===")
    for _ in range(3):
        print(generuj_produkt())
