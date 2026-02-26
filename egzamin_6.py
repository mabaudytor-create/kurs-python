# Utwórz macierz 4x4 z losowymi liczbami całkowitymi od 1 do 100.
# Następnie wyświetl jej kształt, sumę wszystkich elementów, średnią,
# element maksymalny i minimalny, pierwszą kolumnę
# oraz elementy większe niż 50

import numpy as np

# macierz 4x4 z losowymi liczbami 1–100
macierz = np.random.randint(1, 101, size=(4, 4))

print("Macierz:\n", macierz)

# kształt macierzy
print("\nKształt:", macierz.shape)

# suma elementów
print("Suma:", macierz.sum())

# średnia
print("Średnia:", macierz.mean())

# max i min
print("Maksimum:", macierz.max())
print("Minimum:", macierz.min())

# pierwsza kolumna
print("Pierwsza kolumna:\n", macierz[:, 0])

# elementy większe niż 50
print("Elementy > 50:\n", macierz[macierz > 50])

# Dwie macierze 3x3 i wykonaj na nich dodawanie, mnożenie element po elemencie
# oraz mnożenie macierzowe (np.dot). Wyświetl wyniki


import numpy as np

# tworzenie dwóch macierzy 3x3
A = np.random.randint(1, 10, (3, 3))
B = np.random.randint(1, 10, (3, 3))

print("Macierz A:\n", A)
print("\nMacierz B:\n", B)

# 1. dodawanie
dodawanie = A + B
print("\nDodawanie (A + B):\n", dodawanie)

# 2. mnożenie element po elemencie (Hadamarda)
mnozenie_elementowe = A * B
print("\nMnożenie elementowe (A * B):\n", mnozenie_elementowe)

# 3. mnożenie macierzowe (iloczyn macierzy)
mnozenie_macierzowe = np.dot(A, B)
print("\nMnożenie macierzowe (A · B):\n", mnozenie_macierzowe)
