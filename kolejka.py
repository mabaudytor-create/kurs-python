import heapq

class KolejkaPrzychodni:
    def __init__(self):
        self._kolejka = []
        self._licznik = 0  # zabezpieczenie FIFO w obrębie tego samego priorytetu

    def dodaj_pacjenta(self, imie, priorytet):
        heapq.heappush(self._kolejka, (priorytet, self._licznik, imie))
        self._licznik += 1

    def obsluz_pacjenta(self):
        if not self._kolejka:
            return None
        return heapq.heappop(self._kolejka)[2]
