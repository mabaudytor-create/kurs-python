# Definicja funkcji
def przywitaj(imie):

    print("Cześć,", imie, "! Witaj w kursie Pythona!")

# Wywołanie funkcji
przywitaj("Mirek")
przywitaj("Anna")
przywitaj("Piotr")

# Funkcja z wynikiem (return)
def dodaj(a, b):
    wynik = a + b
    return wynik
suma = dodaj(5, 3)

print("5 + 3 =", suma)
