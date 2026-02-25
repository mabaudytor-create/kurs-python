## Typy danych i operatory w Pythonie
# Liczba całkowita (int)
wiek = 77
print(type(wiek))        # <class 'int'>

# Liczba zmiennoprzecinkowa (float)
wzrost = 1.83
print(type(wzrost))      # <class 'float'>

# Tekst (str)
imie = "Mirek"
print(type(imie))        # <class 'str'>

# Prawda/Fałsz (bool)
czy_student = True
print(type(czy_student)) # <class 'bool'>

# Brak wartości (NoneType)
nic = None
print(type(nic))         # <class 'NoneType'>

#  Konwersja typów (casting) Czasami trzeba zamienić wartość z jednego typu na inny.
#  Zamiana tekstu na liczbę
tekst = "42"
liczba = int(tekst)
print(liczba + 8)        # 50
# Zamiana liczby na tekst
wiek = 77
tekst = str(wiek)
print("Mam " + tekst + " lat")   # Mam 77 lat

# Zamiana na float
liczba = float("3.14")
print(liczba)            # 3.14

# Zamiana na bool
print(bool(0))           # False
print(bool(1))           # True
print(bool(""))          # False – pusty tekst to False
print(bool("Mirek"))     # True – niepusty tekst to True

wiek = 77
# print("Mam " + wiek + " lat")       # ❌ BŁĄD!
print("Mam " + str(wiek) + " lat")  # ✅ OK
print(f"Mam {wiek} lat")            # ✅ OK – f-string robi to automatycznie

# Operatory przypisania. Skróty do modyfikowania wartości zmiennej
# – bardzo często używane w pętlach.
liczba = 10
liczba += 5     # to samo co: liczba = liczba + 5  → 15
liczba -= 3     # to samo co: liczba = liczba - 3  → 12
liczba *= 2     # to samo co: liczba = liczba * 2  → 24
liczba /= 4     # to samo co: liczba = liczba / 4  → 6.0
liczba //= 2    # to samo co: liczba = liczba // 2 → 3.0
liczba **= 3    # to samo co: liczba = liczba ** 3 → 27.0
liczba %= 5     # to samo co: liczba = liczba % 5  → 2.0
print(liczba)

# Operatory na tekstach (str)
# Teksty mają swoje własne operacje:
imie = "Mirek"
nazwisko = "Kowalski"

# Łączenie tekstów
pelne_imie = imie + " " + nazwisko
print(pelne_imie)           # Mirek Kowalski

# Powtarzanie tekstu
print("Ha" * 3)             # HaHaHa

# Długość tekstu
print(len(imie))            # 5

# Wielkie i małe litery
print(imie.upper())         # MIREK
print(imie.lower())         # mirek

# Sprawdzanie czy tekst zawiera coś
print("ire" in imie)        # True
print("xyz" in imie)        # False

# Wycinanie fragmentu tekstu (indeksowanie)
print(imie[0])              # M  – pierwsza litera (Python liczy od 0!)
print(imie[1])              # i
print(imie[-1])             # k  – ostatnia litera
print(imie[1:3])            # ir – litery od indeksu 1 do 2
