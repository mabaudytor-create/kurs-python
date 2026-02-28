import redis

# Połączenie z Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

KLUCZ_LICZNIKA = "licznik_stron"


def odwiedz_strone(nazwa_strony: str) -> None:
    """
    Zwiększa licznik odwiedzin dla danej strony.
    Operacja O(log n) w Sorted Set.
    """
    redis_client.zincrby(KLUCZ_LICZNIKA, 1, nazwa_strony)


def top_strony(n: int):
    """
    Zwraca n najpopularniejszych stron
    w postaci listy (nazwa_strony, liczba_odwiedzin).
    """
    wyniki = redis_client.zrevrange(
        KLUCZ_LICZNIKA,
        0,
        n - 1,
        withscores=True
    )

    return [(strona, int(licznik)) for strona, licznik in wyniki]


# =============================
# Przykład użycia
# =============================
if __name__ == "__main__":
    odwiedz_strone("strona_glowna")
    odwiedz_strone("kontakt")
    odwiedz_strone("strona_glowna")
    odwiedz_strone("blog")
    odwiedz_strone("strona_glowna")
    odwiedz_strone("kontakt")

    print("TOP 3 strony:")
    print(top_strony(3))

