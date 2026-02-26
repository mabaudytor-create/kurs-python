
import operacje

a = 10
b = 5

print("Dodawanie:", operacje.dodaj(a, b))
print("Odejmowanie:", operacje.odejmij(a, b))
print("Mnożenie:", operacje.pomnoz(a, b))
print("Dzielenie:", operacje.podziel(a, b))

import operacje

print(operacje.dodaj(10, 5))  # 15
print(operacje.podziel(10, 0))  # Zrzuci ZeroDivisionError

import random

# komputer losuje liczbę od 1 do 100
liczba = random.randint(1, 100)

print("Witaj w grze 'Zgadnij liczbę'!")
print("Komputer wylosował liczbę od 1 do 100.")

# zmienna do śledzenia, czy zgadnięto
zgadnieto = False

while not zgadnieto:
    # pobranie liczby od użytkownika
    try:
        strzal = int(input("Podaj swoją propozycję: "))
    except ValueError:
        print("Podaj poprawną liczbę całkowitą!")
        continue
    # porównanie
    if strzal < liczba:
        print("Za mało!")
    elif strzal > liczba:
        print("Za dużo!")
    else:
        print("Zgadłeś!")
        zgadnieto = True


import random

# komputer losuje liczbę od 1 do 100
liczba = random.randint(1, 100)

print("Witaj w grze 'Zgadnij liczbę'!")
print("Komputer wylosował liczbę od 1 do 100.")

# zmienne
zgadnieto = False
liczba_prob = 0

while not zgadnieto:
    try:
        strzal = int(input("Podaj swoją propozycję: "))
    except ValueError:
        print("Podaj poprawną liczbę całkowitą!")
        continue

    liczba_prob += 1  # zwiększamy licznik prób

    if strzal < liczba:
        print("Za mało!")
    elif strzal > liczba:
        print("Za dużo!")
    else:
        zgadnieto = True
        print(f"Zgadłeś w {liczba_prob} próbach!")  # komunikat po zgadnięciu
