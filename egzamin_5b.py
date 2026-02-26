
from datetime import datetime, date

# aktualna data i czas
teraz = datetime.now()

# polskie nazwy dni tygodnia (poniedziałek = 0)
dni_tygodnia = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]

# wyświetlenie aktualnej daty i godziny
print("Aktualna data i godzina:", teraz.strftime("%Y-%m-%d %H:%M:%S"))

# dzień tygodnia po polsku
dzien = dni_tygodnia[teraz.weekday()]
print("Dzień tygodnia:", dzien)

# ile dni do końca roku
koniec_roku = date(teraz.year, 12, 31)
roznica = (koniec_roku - teraz.date()).days
print("Pozostało dni do końca roku:", roznica)


from datetime import datetime, date

# aktualna data i czas
teraz = datetime.now()

# polskie nazwy dni tygodnia i miesięcy
dni_tygodnia = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
miesiace = ["Stycznia", "Lutego", "Marca", "Kwietnia", "Maja", "Czerwca",
            "Lipca", "Sierpnia", "Września", "Października", "Listopada", "Grudnia"]

# składanie pełnej daty po polsku
dzien_tyg = dni_tygodnia[teraz.weekday()]
dzien_mies = teraz.day
miesiac = miesiace[teraz.month - 1]
rok = teraz.year
godzina = teraz.strftime("%H:%M:%S")

print(f"Dzisiaj jest {dzien_tyg}, {dzien_mies} {miesiac} {rok}, godzina {godzina}")

# ile dni do końca roku
koniec_roku = date(rok, 12, 31)
dni_do_konca = (koniec_roku - teraz.date()).days
print(f"Pozostało dni do końca roku: {dni_do_konca}")
