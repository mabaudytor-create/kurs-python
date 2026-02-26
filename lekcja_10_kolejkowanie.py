# Kolejka w czystym Pythonie

from collections import deque

# Tworzenie kolejki
kolejka = deque()

# Dodawanie elementów na koniec (enqueue)
kolejka.append("Zamówienie nr 1")
kolejka.append("Zamówienie nr 2")
kolejka.append("Zamówienie nr 3")

print("Kolejka:", kolejka)
# deque(['Zamówienie nr 1', 'Zamówienie nr 2', 'Zamówienie nr 3'])

# Pobieranie elementów z początku (dequeue) – FIFO
pierwszy = kolejka.popleft()
print("Obsługuję:", pierwszy)    # Obsługuję: Zamówienie nr 1

print("Pozostało:", kolejka)
# deque(['Zamówienie nr 2', 'Zamówienie nr 3'])

# Sprawdzenie czy kolejka jest pusta
print("Czy pusta:", len(kolejka) == 0)    # False

# Kolejka priorytetowa
# Czasem nie chodzi o kolejność zgłoszenia ale o ważność zadania.
# Pacjent z zawałem jest obsługiwany przed pacjentem z katarem
# - to kolejka priorytetowa

import heapq

kolejka = []

# Dodawanie (priorytet, zadanie) – niższy numer = wyższy priorytet
heapq.heappush(kolejka, (3, "Zwykłe zamówienie"))
heapq.heappush(kolejka, (1, "Pilna dostawa"))
heapq.heappush(kolejka, (2, "Ekspresowa wysyłka"))

print("Kolejność obsługi:")
while kolejka:
    priorytet, zadanie = heapq.heappop(kolejka)
    print(f"  Priorytet {priorytet}: {zadanie}")

# Priorytet 1: Pilna dostawa
# Priorytet 2: Ekspresowa wysyłka
# Priorytet 3: Zwykłe zamówienie


# Kolejkowanie z SQLite.SQLite to lekka baza danych przechowywana
# w jednym pliku na dysku. Idealna do nauki i małych projektów
# – nie wymaga instalacji serwera




