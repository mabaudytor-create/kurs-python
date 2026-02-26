import unittest
from kolejka import KolejkaPrzychodni


class TestKolejkaPrzychodni(unittest.TestCase):

    def setUp(self):
        self.kolejka = KolejkaPrzychodni()

    def test_pilny_przed_zwyklym_mimo_pozniejszego_zgloszenia(self):
        """
        Pacjent zwykły zgłasza się pierwszy,
        pacjent pilny zgłasza się później,
        ale powinien zostać obsłużony jako pierwszy.
        """
        self.kolejka.dodaj_pacjenta("Jan", 2)      # zwykły
        self.kolejka.dodaj_pacjenta("Anna", 1)     # pilny

        pierwszy = self.kolejka.obsluz_pacjenta()

        self.assertEqual(pierwszy, "Anna")

    def test_fifo_dla_tego_samego_priorytetu(self):
        """
        Jeżeli pacjenci mają ten sam priorytet,
        kolejność obsługi powinna być zgodna z kolejnością zgłoszeń.
        """
        self.kolejka.dodaj_pacjenta("Jan", 2)
        self.kolejka.dodaj_pacjenta("Piotr", 2)

        pierwszy = self.kolejka.obsluz_pacjenta()
        drugi = self.kolejka.obsluz_pacjenta()

        self.assertEqual(pierwszy, "Jan")
        self.assertEqual(drugi, "Piotr")

    def test_wielu_pilnych_i_zwyklych(self):
        """
        Weryfikacja stabilności algorytmu przy wielu elementach.
        """
        self.kolejka.dodaj_pacjenta("Jan", 2)
        self.kolejka.dodaj_pacjenta("Anna", 1)
        self.kolejka.dodaj_pacjenta("Piotr", 2)
        self.kolejka.dodaj_pacjenta("Maria", 1)

        wyniki = [
            self.kolejka.obsluz_pacjenta(),
            self.kolejka.obsluz_pacjenta(),
            self.kolejka.obsluz_pacjenta(),
            self.kolejka.obsluz_pacjenta(),
        ]

        self.assertEqual(wyniki, ["Anna", "Maria", "Jan", "Piotr"])

    def test_pusta_kolejka(self):
        """
        Obsługa przypadku brzegowego – brak pacjentów.
        """
        self.assertIsNone(self.kolejka.obsluz_pacjenta())


if __name__ == "__main__":
    unittest.main()
