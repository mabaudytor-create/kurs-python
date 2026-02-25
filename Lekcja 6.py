# Operatory arytmetyczne Służą do wykonywania podstawowych działań matematycznych.
a = 10
b = 3
print(a + b)    # 13  – dodawanie
print(a - b)    # 7   – odejmowanie
print(a * b)    # 30  – mnożenie
print(a / b)    # 3.3333... – dzielenie (zawsze zwraca float)
print(a // b)   # 3   – dzielenie całkowite (bez reszty)
print(a % b)    # 1   – reszta z dzielenia (modulo)
print(a ** b)   # 1000 – potęgowanie (10 do potęgi 3)

#  Operatory porównania Służą do porównywania wartości
#  – zwracają True lub False w zależności od wyniku porównania.
a = 10
b = 3
print(a == b)   # False – czy równe?
print(a != b)   # True  – czy różne?
print(a > b)    # True  – czy większe?
print(a < b)    # False – czy mniejsze?
print(a >= b)   # True  – czy większe lub równe?
print(a <= b)   # False – czy mniejsze lub równe?

#  Operatory logiczne Służą do łączenia warunków
#  – przydatne gdy chcesz sprawdzić kilka rzeczy naraz.
wiek = 77
miasto = "Łódź"

# and – oba warunki muszą być prawdziwe
if wiek > 18 and miasto == "Łódź":
    print("Dorosły z Łodzi")

# or – wystarczy jeden warunek prawdziwy
if wiek > 18 or miasto == "Warszawa":
    print("Dorosły LUB z Warszawy")

# not – odwraca warunek
if not wiek < 18:
    print("Na pewno nie jest niepełnoletni")
