import redis
import json
import time

# Połączenie z Redis
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True  # automatycznie dekoduje bytes na string
)

# Sprawdzenie połączenia
print("Połączono z Redis:", r.ping())  # True

# =========================================================
# CZYSZCZENIE DANYCH Z POPRZEDNICH URUCHOMIEŃ
# =========================================================
r.delete("imie", "sesja_123", "licznik_wizyt", "kolejka",
         "uzytkownik:1", "cache:user:1")
print("✅ Wyczyszczono poprzednie dane")

# =========================================================
# PODSTAWOWE OPERACJE
# =========================================================

# SET i GET – ustawianie i pobieranie wartości
r.set("imie", "Mirek")
print("\n--- SET/GET ---")
print(r.get("imie"))              # Mirek

# SET z TTL (Time To Live) – wartość wygasa po X sekundach
r.set("sesja_123", "zalogowany", ex=30)
print("TTL sesji:", r.ttl("sesja_123"))   # np. 29

# Sprawdzenie czy klucz istnieje
print("Czy istnieje 'imie':", r.exists("imie"))   # 1
print("Czy istnieje 'xyz':", r.exists("xyz"))     # 0

# Usuwanie klucza
r.delete("imie")
print("Po usunięciu 'imie':", r.exists("imie"))   # 0

# =========================================================
# LICZNIKI
# =========================================================
print("\n--- LICZNIKI ---")
r.set("licznik_wizyt", 0)
r.incr("licznik_wizyt")
r.incr("licznik_wizyt")
r.incr("licznik_wizyt")
print("Licznik wizyt:", r.get("licznik_wizyt"))   # 3

# =========================================================
# LISTY
# =========================================================
print("\n--- LISTY ---")
r.rpush("kolejka", "zadanie_1")
r.rpush("kolejka", "zadanie_2")
r.rpush("kolejka", "zadanie_3")

print("Długość kolejki:", r.llen("kolejka"))              # 3
print("Wszystkie elementy:", r.lrange("kolejka", 0, -1))  # 3 elementy

# Pobieranie z początku (FIFO)
zadanie = r.lpop("kolejka")
print("Pobrano:", zadanie)    # zadanie_1
print("Pozostało:", r.lrange("kolejka", 0, -1))

# =========================================================
# SŁOWNIKI (HASH) – poprawiona wersja
# =========================================================
print("\n--- HASH ---")

# Poprawka – używamy hset z osobnymi parami klucz/wartość
r.hset("uzytkownik:1", "imie", "Mirek")
r.hset("uzytkownik:1", "email", "mirek@email.com")
r.hset("uzytkownik:1", "wiek", "77")

print("Imię:", r.hget("uzytkownik:1", "imie"))       # Mirek
print("Wszystko:", r.hgetall("uzytkownik:1"))         # cały słownik

# =========================================================
# CACHE – praktyczny przykład
# =========================================================
print("\n--- CACHE ---")


def pobierz_dane_z_bazy(user_id):
    """Symulacja wolnego zapytania do bazy danych."""
    print(f"  [BAZA] Pobieranie danych użytkownika {user_id}...")
    time.sleep(2)  # symulacja wolnego zapytania
    return {"id": user_id, "imie": "Mirek", "email": "mirek@email.com"}


def pobierz_uzytkownika(user_id):
    """Pobiera użytkownika – najpierw sprawdza cache."""
    klucz = f"cache:user:{user_id}"

    # Sprawdź czy jest w cache
    dane = r.get(klucz)
    if dane:
        print("  [CACHE] Dane z cache!")
        return json.loads(dane)

    # Nie ma w cache – pobierz z bazy i zapisz do cache
    uzytkownik = pobierz_dane_z_bazy(user_id)
    r.set(klucz, json.dumps(uzytkownik), ex=60)  # cache na 60 sekund
    return uzytkownik


print("Pierwsze pobranie (z bazy – wolne):")
u = pobierz_uzytkownika(1)
print(" ", u)

print("\nDrugie pobranie (z cache – szybkie):")
u = pobierz_uzytkownika(1)
print(" ", u)

