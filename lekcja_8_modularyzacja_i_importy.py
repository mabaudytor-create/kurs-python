# NPEP8 to oficjalny przewodnik stylu pisania kodu w Pythonie.
# Najważniejsze zasady PEP8

# Nazewnictwo
# ❌ ŹLE
from matematyka import pole_prostokata
import matematyka
import os
import datetime
import random
import math as m
from math import sqrt, pi
import math
ImieUzytkownika = "Mirek"
WIEK = 77


def ObliczPole(a, b):
    return a * b


# ✅ DOBRZE
imie_uzytkownika = "Mirek"  # zmienne: małe_litery_z_podkreśleniem
MAKS_WIEK = 120  # stałe: WIELKIE_LITERY


def oblicz_pole(a, b):  # funkcje: małe_litery_z_podkreśleniem
    return a * b


class KontoBankowe:  # klasy: WielkieLitery (CamelCase)
    pass


# Spacje i wcięcia
# ❌ ŹLE
x = 10
y = x + 5
if x > 5:
    print(x)
# ✅ DOBRZE
x = 10  # spacje wokół operatorów
y = x + 5
if x > 5:
    print(x)  # 4 spacje wcięcia (nie Tab!)

# Długość linii i puste linie

# ❌ ŹLE – za długa linia
imie_i_nazwisko_uzytkownika = input(
    "Podaj swoje pełne imię i nazwisko bez polskich znaków: Mirek Kowalski")

# ✅ DOBRZE – max 79 znaków w linii
pytanie = "Podaj swoje pełne imię i nazwisko: Mirek Kowalski"
imie_i_nazwisko = input(pytanie)

# Można przechwycić przerwanie:
try:
    imie = input(
        "Podaj swoje pełne imię i nazwisko bez polskich znaków: Mirk Kowalski")
    print("Wpisałeś:", imie)
except KeyboardInterrupt:
    print("\nPrzerwano wprowadzanie danych.")


# Dwie puste linie między klasami i funkcjami najwyższego poziomu
class Pierwsza:
    pass


class Druga:
    pass


# Jedna pusta linia między metodami w klasie
class Przyklad:
    def metoda_pierwsza(self):
        pass

    def metoda_druga(self):
        pass


# Komentarze
# ❌ ŹLE
x = x + 1  # zwiększenie x o 1 (komentarz oczywisty – nie wnosi nic)

# ✅ DOBRZE
x = x + 1  # kompensacja przesunięcia o jeden piksel (wyjaśnia DLACZEGO)


# Docstring – opis funkcji w potrójnych cudzysłowach
def oblicz_pole(szerokosc, wysokosc):
    """Oblicza pole prostokąta.
    Args:
        szerokosc: szerokość prostokąta w cm
  Returns:
        Pole prostokąta w cm²
    """
    return szerokosc * wysokość


# Modularyzacja to dzielenie kodu na osobne pliki według tematyki.
# Łatwiej znaleźć błąd gdy wiesz w którym pliku szukać
# Możesz używać tego samego kodu w wielu projektach
# Zespół programistów może pracować na różnych plikach jednocześnie

# Import to sposób na użycie kodu z innego pliku lub biblioteki.
# Importowanie bibliotek standardowych
# Python ma wbudowane biblioteki których możesz używać od razu

# Importowanie całej biblioteki

print(math.pi)  # 3.141592653589793
print(math.sqrt(16))  # 4.0 – pierwiastek kwadratowy
print(math.ceil(3.2))  # 4 – zaokrąglenie w górę
print(math.floor(3.8))  # 3 – zaokrąglenie w dół

# Importowanie konkretnej funkcji z biblioteki

print(sqrt(25))  # 5.0 – bez przedrostka math.
print(pi)  # 3.141592653589793

# Importowanie z aliasem (skróconą nazwą)

print(m.sqrt(9))  # 3.0

# Inne przydatne biblioteki standardowe

print(random.randint(1, 10))  # losowa liczba od 1 do 10
print(random.choice(["a", "b", "c"]))  # losowy element z listy


teraz = datetime.datetime.now()
print(teraz)  # aktualna data i czas
print(teraz.year)  # 2026
print(teraz.strftime("%d.%m.%Y"))  # 26.02.2026


print(os.getcwd())  # aktualny folder
print(os.listdir("."))  # lista plików w folderze

# Importowanie własnych plików
# To jest sedno modularyzacji – używasz kodu który sam napisałeś w innym pliku.
# Stwórz plik matematyka.py:

"""Moduł z funkcjami matematycznymi."""
PI = 3.14159


def pole_kola(promien):
    """Oblicza pole koła."""
    return PI * promien ** 2


def obwod_kola(promien):
    """Oblicza obwód koła."""
    return 2 * PI * promien


def pole_prostokata(a, b):
    """Oblicza pole prostokąta."""
    return a * b


# Teraz stwórz plik program.py w tym samym folderze:
"""Główny program używający modułu matematyka."""


# Użycie przez nazwę modułu
print(matematyka.pole_kola(5))  # 78.53975
print(matematyka.obwod_kola(5))  # 31.4159

# Użycie bezpośrednie (dzięki from...import)
print(pole_prostokata(4, 6))  # 24

# Dostęp do stałej z modułu
print(matematyka.PI)  # 3.14159


# if __name__ == "__main__"

# matematyka.py

def pole_kola(promien):
    return 3.14 * promien ** 2


# Ten blok uruchomi się TYLKO gdy uruchamiasz ten plik bezpośrednio
# NIE uruchomi się gdy importujesz ten plik w innym miejscu
if __name__ == "__main__":
    # kod testowy – uruchamia się tylko podczas bezpośredniego uruchomienia
    print("Test:", pole_kola(5))

# Dzięki temu możesz testować moduł uruchamiając go bezpośrednio,
# ale gdy importujesz go w innym pliku, ten testowy kod się nie wykona.
# To jest bardzo przydatne!
