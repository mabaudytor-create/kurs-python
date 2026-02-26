import unittest
from gra import sprawdz_strzal

class TestZgadnijLiczbe(unittest.TestCase):

    def test_za_malo(self):
        self.assertEqual(sprawdz_strzal(50, 20), "za mało")

    def test_za_duzo(self):
        self.assertEqual(sprawdz_strzal(50, 80), "za dużo")

    def test_zgadles(self):
        self.assertEqual(sprawdz_strzal(50, 50), "zgadłeś")


if __name__ == "__main__":
    unittest.main()
