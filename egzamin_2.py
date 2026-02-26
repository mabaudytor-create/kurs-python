# Napisz funkcję kalkulator(a, b, dzialanie) która w zależności od parametru
# dzialanie ("dodawanie", "odejmowanie", "mnozenie") zwraca odpowiedni wynik.

def kalkulator(a, b, dzialanie):
    if dzialanie == "dodawanie":
        return a + b
    elif dzialanie == "odejmowanie":
        return a - b
    elif dzialanie == "mnozenie":
        return a * b
    elif dzialanie == "dzielenie":
        if b == 0:
            return "Błąd – nie można dzielić przez zero!"
        return a / b
    else:
        return "Nieznane działanie"


print(kalkulator(3, 2, "dodawanie"))  # 5
print(kalkulator(3, 2, "odejmowanie"))  # 1
print(kalkulator(3, 2, "mnozenie"))  # 6
print(kalkulator(3, 2, "dzielenie"))  # 1.5
