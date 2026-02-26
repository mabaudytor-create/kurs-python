import unittest
from prostokat import Prostokat   # plik prostokat.py

class TestProstokat(unittest.TestCase):

    # ---- TESTY POLA ----
    def test_pole_typowe(self):
        p = Prostokat(3, 4)
        self.assertEqual(p.pole(), 12)

    def test_pole_kwadrat(self):
        p = Prostokat(5, 5)
        self.assertEqual(p.pole(), 25)

    def test_pole_zero(self):
        p = Prostokat(0, 10)
        self.assertEqual(p.pole(), 0)

    def test_pole_dwa_zera(self):
        p = Prostokat(0, 0)
        self.assertEqual(p.pole(), 0)

    # ---- TESTY OBWODU ----
    def test_obwod_typowy(self):
        p = Prostokat(3, 4)
        self.assertEqual(p.obwod(), 14)

    def test_obwod_kwadrat(self):
        p = Prostokat(5, 5)
        self.assertEqual(p.obwod(), 20)

    def test_obwod_zero(self):
        p = Prostokat(0, 10)
        self.assertEqual(p.obwod(), 20)

    def test_obwod_dwa_zera(self):
        p = Prostokat(0, 0)
        self.assertEqual(p.obwod(), 0)


if __name__ == "__main__":
    unittest.main()
