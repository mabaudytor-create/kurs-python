# Macierze i NumPy

# Bez NumPy – musisz pisać pętlę
lista = [1, 2, 3, 4, 5]
lista2 = [x * 2 for x in lista]    # [2, 4, 6, 8, 10]

# Z NumPy – operacja na całej tablicy naraz
import numpy as np
tablica = np.array([1, 2, 3, 4, 5])
tablica2 = tablica * 2              # [2, 4, 6, 8, 10] – prościej i szybciej!


# Podstawy NumPy
import numpy as np

# Tworzenie tablicy 1D (wektor)
tablica = np.array([1, 2, 3, 4, 5])
print(tablica)           # [1 2 3 4 5]
print(type(tablica))     # <class 'numpy.ndarray'>
print(tablica.shape)     # (5,) – 5 elementów, 1 wymiar
print(tablica.dtype)     # int64 – typ danych

# Tworzenie tablicy 2D (macierz)
macierz = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print(macierz)
print(macierz.shape)     # (3, 3) – 3 wiersze, 3 kolumny


# Tworzenie specjalnych tablic
import numpy as np

# Tablica samych zer
zera = np.zeros((3, 4))         # 3 wiersze, 4 kolumny
print(zera)

# Tablica samych jedynek
jedynki = np.ones((2, 3))
print(jedynki)

# Macierz jednostkowa (jedynki na przekątnej)
jednostkowa = np.eye(3)
print(jednostkowa)

# Tablica z zakresu (jak range ale NumPy)
zakres = np.arange(0, 10, 2)    # od 0 do 10 co 2
print(zakres)                   # [0 2 4 6 8]

# Tablica równomiernie rozłożonych wartości
liniowa = np.linspace(0, 1, 5)  # 5 wartości od 0 do 1
print(liniowa)                  # [0.   0.25 0.5  0.75 1.  ]

# Tablica losowych liczb
losowe = np.random.randint(0, 10, size=(3, 3))
print(losowe)

# Operacje na macierzach

import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# Operacje element po elemencie
print(a + b)        # [11 22 33 44 55]
print(a * b)        # [ 10  40  90 160 250]
print(a ** 2)       # [ 1  4  9 16 25]
print(b / a)        # [10. 10. 10. 10. 10.]

# Operacje statystyczne
print(a.sum())      # 15  – suma
print(a.mean())     # 3.0 – średnia
print(a.min())      # 1   – minimum
print(a.max())      # 5   – maksimum
print(a.std())      # odchylenie standardowe

# Operacje na macierzach 2D
m1 = np.array([[1, 2], [3, 4]])
m2 = np.array([[5, 6], [7, 8]])

# Mnożenie macierzowe (nie element po elemencie!)
print(np.dot(m1, m2))
# [[19 22]
#  [43 50]]

# Transpozycja (zamiana wierszy z kolumnami)
print(m1.T)
# [[1 3]
#  [2 4]]

# Reshape – zmiana kształtu
import numpy as np

# Tworzenie tablicy 1D z 12 elementów
tablica = np.arange(1, 13)
print(tablica)          # [ 1  2  3  4  5  6  7  8  9 10 11 12]

# Zmiana na macierz 3x4
macierz = tablica.reshape(3, 4)
print(macierz)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]

# Zmiana na macierz 2x6
print(tablica.reshape(2, 6))

# Spłaszczenie z powrotem do 1D
print(macierz.flatten())    # [ 1  2  3  4  5  6  7  8  9 10 11 12]

# Najważniejsze metody assert

# Sprawdzanie równości
self.assertEqual(wynik, 8)          # wynik == 8
self.assertNotEqual(wynik, 5)       # wynik != 5

# Sprawdzanie prawdy/fałszu
self.assertTrue(wynik > 0)          # wynik jest prawdziwy
self.assertFalse(wynik < 0)         # wynik jest fałszywy

# Sprawdzanie None
self.assertIsNone(wynik)            # wynik jest None
self.assertIsNotNone(wynik)         # wynik nie jest None

# Sprawdzanie wyjątków
with self.assertRaises(ValueError):
    funkcja_ktora_rzuca_wyjatek()

# Sprawdzanie przybliżonej równości (dla float!)
self.assertAlmostEqual(3.14159, 3.14, places=2)


# setUp i tearDown to specjalne metody w unittest
# które uruchamiają się przed i po każdym teście.
class TestSklep(unittest.TestCase):

    def setUp(self):
        """Uruchamia się przed każdym testem – przygotowuje dane."""
        self.sklep = Sklep()
        self.sklep.dodaj_produkt("Chleb", 4.50)
        self.sklep.dodaj_produkt("Mleko", 3.20)

    def tearDown(self):
        """Uruchamia się po każdym teście – sprząta po sobie."""
        pass  # tutaj np. zamknięcie połączenia z bazą danych

    def test_liczba_produktow(self):
        # sklep już ma dwa produkty dzięki setUp
        self.assertEqual(len(self.sklep._Sklep__produkty), 2)

    def test_znajdz_istniejacy_produkt(self):
        wynik = self.sklep.znajdz_produkt("Chleb")
        self.assertIsNotNone(wynik)

    def test_znajdz_nieistniejacy_produkt(self):
        wynik = self.sklep.znajdz_produkt("Złoto")
        self.assertIsNone(wynik)

