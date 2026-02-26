"""Testy jednostkowe dla modułu operacje."""
import unittest
import operacje


class TestOperacje(unittest.TestCase):

    # Każda metoda testowa musi zaczynać się od słowa "test"!

    def test_dodaj_liczby_dodatnie(self):
        wynik = operacje.dodaj(3, 5)
        self.assertEqual(wynik, 8)      # sprawdza czy wynik == 8

    def test_dodaj_liczby_ujemne(self):
        wynik = operacje.dodaj(-3, -5)
        self.assertEqual(wynik, -8)

    def test_dodaj_zero(self):
        wynik = operacje.dodaj(5, 0)
        self.assertEqual(wynik, 5)

    def test_odejmij(self):
        self.assertEqual(operacje.odejmij(10, 3), 7)

    def test_pomnoz(self):
        self.assertEqual(operacje.pomnoz(4, 5), 20)

    def test_podziel(self):
        self.assertEqual(operacje.podziel(10, 2), 5.0)

    def test_podziel_przez_zero(self):
        # Sprawdzamy czy funkcja rzuca wyjątek ValueError
        with self.assertRaises(ValueError):
            operacje.podziel(10, 0)


if __name__ == "__main__":
    unittest.main()
