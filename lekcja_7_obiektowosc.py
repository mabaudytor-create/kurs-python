class Samochod:
    # __init__ to konstruktor – uruchamia się gdy tworzysz obiekt
    def __init__(self, marka, kolor, rok):
        self.marka = marka  # atrybut obiektu
        self.kolor = kolor  # atrybut obiektu
        self.rok = rok  # atrybut obiektu

    # metoda – funkcja należąca do klasy
    def przedstaw_sie(self):
        print(f"Jestem {self.kolor} {self.marka} z roku {self.rok}")

    def oblicz_wiek(self):
        wiek = 2026 - self.rok
        print(f"Ten samochód ma {wiek} lat")


# Tworzenie obiektów
auto1 = Samochod("Fiat", "czerwony", 2015)
auto2 = Samochod("BMW", "czarny", 2020)
auto3 = Samochod("Toyota", "biały", 2010)

# Wywołanie metod
auto1.przedstaw_sie()  # Jestem czerwony Fiat z roku 2015
auto2.przedstaw_sie()  # Jestem czarny BMW z roku 2020
auto1.oblicz_wiek()  # Ten samochód ma 11 lat

# Dostęp do atrybutów
print(auto1.marka)  # Fiat
print(auto2.kolor)  # czarny


class KontoBankowe:
    def __init__(self, wlasciciel, saldo):
        self.wlasciciel = wlasciciel
        self.__saldo = saldo  # __ = prywatny, chroniony atrybut

    def wplac(self, kwota):
        if kwota > 0:
            self.__saldo += kwota
            print(f"Wpłacono {kwota} zł. Saldo: {self.__saldo} zł")

    def wyplac(self, kwota):
        if kwota > self.__saldo:
            print("Brak środków!")
        else:
            self.__saldo -= kwota
            print(f"Wypłacono {kwota} zł. Saldo: {self.__saldo} zł")

    def sprawdz_saldo(self):
        print(f"Saldo konta {self.wlasciciel}: {self.__saldo} zł")


konto = KontoBankowe("Mirek", 1000)
konto.wplac(500)  # Wpłacono 500 zł. Saldo: 1500 zł
konto.wyplac(200)  # Wypłacono 200 zł. Saldo: 1300 zł
konto.sprawdz_saldo()  # Saldo konta Mirek: 1300 zł

# To zadziała:
print(konto.wlasciciel)  # Mirek


# To nie zadziała – saldo jest prywatne!
# print(konto.__saldo)    # ❌ BŁĄD

# Dziedziczenie – przejmowanie cech
#  Dziedziczenie – tworzenie nowych klas na podstawie istniejących


class Zwierze:
    def __init__(self, imie, wiek):
        self.imie = imie
        self.wiek = wiek

    def przedstaw_sie(self):
        print(f"Jestem {self.imie} i mam {self.wiek} lat")


# Pies dziedziczy po Zwierze


class Pies(Zwierze):
    def __init__(self, imie, wiek, rasa):
        super().__init__(imie, wiek)  # wywołuje konstruktor klasy Zwierze
        self.rasa = rasa

    def szczekaj(self):
        print(f"{self.imie} mówi: Hau hau!")


# Kot dziedziczy po Zwierze


class Kot(Zwierze):
    def miaucz(self):
        print(f"{self.imie} mówi: Miau!")


pies = Pies("Burek", 3, "Labrador")
kot = Kot("Mruczek", 5)

pies.przedstaw_sie()  # Jestem Burek i mam 3 lat
pies.szczekaj()  # Burek mówi: Hau hau!
kot.przedstaw_sie()  # Jestem Mruczek i mam 5 lat
kot.miaucz()  # Mruczek mówi: Miau!


# super() oznacza "wywołaj metodę z klasy nadrzędnej (rodzica)".

# Polimorfizm – wiele form
# Polimorfizm – różne klasy mogą mieć metody o tej samej nazwie,
# ale działające inaczej

class Figura:
    def pole(self):
        pass  # pusta metoda – do nadpisania przez klasy potomne


class Prostokat(Figura):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def pole(self):
        return self.a * self.b


class Kolo(Figura):
    def __init__(self, promien):
        self.promien = promien

    def pole(self):
        return 3.14 * self.promien ** 2


figury = [Prostokat(4, 5), Kolo(3), Prostokat(2, 8)]

for figura in figury:
    print(f"Pole figury: {figura.pole()}")


# Pole figury: 20
# Pole figury: 28.26
# Pole figury: 16
# Każda figura ma metodę pole() ale każda liczy ją inaczej –
# – to właśnie polimorfizm!
# Abstrakcja – ukrywanie szczegółów, upraszczanie złóżonści
# Abstrakcja – ukrywanie szczegółów implementacji i pokazywanie tylko tego,
# co jest istotne dla użytkownika

class Ekspres:

    def __init__(self):
        self.__woda = 100
        self.__kawa = 50

    def __podgrzej_wode(self):  # prywatna – ukryta przed użytkownikiem
        print("Podgrzewam wodę...")

    def __zmiel_kawe(self):  # prywatna – ukryta przed użytkownikiem
        print("Mielę kawę...")

    def zrob_kawe(self):  # publiczna – jedyne co widzi użytkownik
        self.__podgrzej_wode()
        self.__zmiel_kawe()
        self.__woda -= 20
        self.__kawa -= 10
        print("Kawa gotowa! ☕")


ekspres = Ekspres()
ekspres.zrob_kawe()  # użytkownik nie wie co dzieje się w środku

# Używasz ekspresu naciskając jeden przycisk – nie musisz wiedzieć
# jak działa środek. To jest abstrakcja!
