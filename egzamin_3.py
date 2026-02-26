# Pobranie dwóch liczb od użytkownika
#  i wykonanie na nich wszystkich podstawowych operacji matematycznych.

a = float(input("Podaj pierwszą liczbę: "))
b = float(input("Podaj drugą liczbę: "))

print(a + b)  # – dodawanie
print(f"{a} + {b} = {a + b}")
print(a - b)  # – odejmowanie
print(f"{a} - {b} = {a - b}")
print(a * b)  # – mnożenie
if b == 0:
    print("Dzielenie: Błąd - nie można dzielić przez zero")
    print("Dzielenie całkowite: Błąd - nie można dzielić przez zero")
    print("Modulo: Błąd - nie można dzielić przez zero")
else:
    print(a / b)      # 3.3333... – dzielenie (zawsze zwraca float)
    print(a // b)     # 3   – dzielenie całkowite (bez reszty)
    print(a % b)    # 1   – reszta z dzielenia (modulo)
print(a ** b)    # 1000 – potęgowanie (10 do potęgi 3)

# Pobranie tekstu od użytkownika i wykonanie na nim różnych operacji:
# - wyświetlenie tekstu wielkimi literami
# - wyświetlenie tekstu małymi literami

# pobranie danych
imie = input("Podaj imię: ")
nazwisko = input("Podaj nazwisko: ")
pelne = imie + " " + nazwisko
# wielkie litery
print("Wielkie litery:", pelne.upper())
# małe litery
print("Małe litery:", pelne.lower())
# liczba znaków bez spacji
bez_spacji = pelne.replace(" ", "")
print("Liczba znaków (bez spacji):", len(bez_spacji))


# pobranie danych
wiek = int(input("Podaj wiek: "))
dochod = float(input("Podaj miesięczny dochód (zł): "))

# sprawdzenie warunków
if wiek >= 18 and wiek <= 65 and dochod > 3000:
    print("Możesz otrzymać kredyt")
else:
    print("Nie spełniasz warunków do kredytu")


# dane wejściowe
c = float(input("Podaj pierwszą liczbę: "))
d = float(input("Podaj drugą liczbę: "))
op = input("Podaj działanie (+, -, *, /): ")

# obliczenia
if op == "+":
    print("Wynik:", c + d)
elif op == "-":
    print("Wynik:", c - d)
elif op == "*":
    print("Wynik:", c * d)
elif op == "/":
    if d == 0:
        print("Błąd: nie można dzielić przez zero")
    else:
        print("Wynik:", c / d)
else:
    print("Nieznane działanie")
