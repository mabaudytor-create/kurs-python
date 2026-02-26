# Stwórz zmienne z Twoim imieniem, wiekiem i miastem,
# a następnie wyświetl zdanie:
# "Moje imię to [imię], mam [wiek] lat i mieszkam w [miasto]."
imie = "Mirek"
wiek = 77
miasto = "Łódź"
print("Moje imię to", imie, "mam", wiek, "lat", "i mieszkam w", miasto)

# Napisz program który sprawdza czy wpisana liczba
# jest parzysta czy nieparzysta.
# (Podpowiedź: użyj operatora % który zwraca resztę z dzielenia
#  – jeśli liczba % 2 == 0 to liczba jest parzysta)

liczba = int(input("Podaj liczbę: "))
if liczba % 2 == 0:
    print("Liczba jest parzysta")
else:
    print("Liczba jest nieparzysta")


# Napisz pętlę która wyświetla liczby od 1 do 10
#  i przy każdej pisze czy jest parzysta czy nieparzysta.
for i in range(1, 11):
    if i % 2 == 0:
        print(i, "jest parzysta")
    else:
        print(i, "jest nieparzysta")
        print(i, "jest nieparzysta")
