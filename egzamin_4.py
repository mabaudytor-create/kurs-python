# Stwórz klasę Osoba z atrybutami imie, nazwisko, wiek
# i metodami przedstaw_sie() oraz czy_dorosly(),
# która która zwraca True lub False

class Osoba:

    def __init__(self, imie, nazwisko, wiek):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek

    def przedstaw_sie(self):
        print(
            f"Nazywam się {self.imie} {self.nazwisko} i mam {self.wiek} lat.")

    def czy_dorosly(self):
        return self.wiek >= 18


# utworzenie obiektu
o = Osoba("Mirek", "Kowalski", 77)

# użycie metod
o.przedstaw_sie()

print("Czy dorosły:", o.czy_dorosly())


# Stwórz klasę Prostokat z atrybutami szerokosc i wysokosc
# oraz metodami pole() i obwod().
# Stwórz trzy różne prostokąty i wyświetl ich pola i obwody.

class Prostokat:

    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

    def pole(self):
        return self.szerokosc * self.wysokosc

    def obwod(self):
        return 2 * (self.szerokosc + self.wysokosc)


# utworzenie trzech prostokątów
p1 = Prostokat(3, 4)
p2 = Prostokat(5, 2)
p3 = Prostokat(7, 6)

# wyświetlenie wyników
for i, p in enumerate([p1, p2, p3], start=1):
    print(f"Prostokąt {i}:")
    print("  Pole =", p.pole())
    print("  Obwód =", p.obwod())


# Stwórz klasę Student która dziedziczy po klasie Osoba z Ćwiczenia 1.
# Dodaj atrybut kierunek i metodę przedstaw_sie()
# tóra wyświetla więcej informacji niż w klasie Osoba.

class Osoba:

    def __init__(self, imie, nazwisko, wiek):
        self.imie = imie
        self.nazwisko = nazwisko
        self.wiek = wiek

    def przedstaw_sie(self):
        print(
            f"Nazywam się {self.imie} {self.nazwisko} i mam {self.wiek} lat.")


class Student(Osoba):

    def __init__(self, imie, nazwisko, wiek, kierunek):
        super().__init__(imie, nazwisko, wiek)
        # wywołanie konstruktora klasy bazowej
        self.kierunek = kierunek

    # nadpisanie metody


def przedstaw_sie(self):
    print(
        f"Jestem {self.imie} {self.nazwisko}, "
        f"mam {self.wiek} lat "
        f"i studiuję kierunek: {self.kierunek}."
    )


s = Student("Anna", "Nowak", 21, "Informatyka")
s.przedstaw_sie()


# Stwórz klasę Sklep z prywatną listą produktów i metodami
# dodaj_produkt(nazwa, cena), wyswietl_produkty() i znajdz_produkt(nazwa).

class Sklep:

    def __init__(self):
        self.__produkty = []  # lista prywatna

    def dodaj_produkt(self, nazwa, cena):
        self.__produkty.append({"nazwa": nazwa, "cena": cena})

    def wyswietl_produkty(self):
        if not self.__produkty:
            print("Brak produktów w sklepie")
            return

        for p in self.__produkty:
            print(f"{p['nazwa']} - {p['cena']} zł")

    def znajdz_produkt(self, nazwa):
        for p in self.__produkty:
            if p["nazwa"].lower() == nazwa.lower():
                return p
        return None


sklep = Sklep()

sklep.dodaj_produkt("Chleb", 4.50)
sklep.dodaj_produkt("Mleko", 3.20)
sklep.dodaj_produkt("Masło", 7.80)

sklep.wyswietl_produkty()

wynik = sklep.znajdz_produkt("mleko")
print("Znaleziono:", wynik)
