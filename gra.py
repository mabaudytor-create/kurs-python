def sprawdz_strzal(liczba, strzal):
    if strzal < liczba:
        return "za mało"
    elif strzal > liczba:
        return "za dużo"
    else:
        return "zgadłeś"
