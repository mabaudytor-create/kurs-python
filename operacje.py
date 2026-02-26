def dodaj(a, b):
    return a + b

def odejmij(a, b):
    return a - b

def pomnoz(a, b):
    return a * b

def podziel(a, b):
    if b == 0:
        return "Błąd: dzielenie przez zero"
    return a / b



def dodaj(a, b):
    """Dodaje dwie liczby."""
    return a + b

def odejmij(a, b):
    """Odejmuje dwie liczby."""
    return a - b

def pomnoz(a, b):
    """Mnoży dwie liczby."""
    return a * b

def podziel(a, b):
    """Dzieli dwie liczby."""
    if b == 0:
        raise ValueError("Nie można dzielić przez zero!")
    return a / b
