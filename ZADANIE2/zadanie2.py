def rzymskie_na_arabskie(rzymskie):
    if not isinstance(rzymskie, str):
        raise ValueError("Liczba rzymska musi być łańcuchem znaków (str).")

    if rzymskie == "":
        raise ValueError("Pusty napis nie jest liczbą rzymską.")

    symbole = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }

    for znak in rzymskie:
        if znak not in symbole:
            raise ValueError(f"Niepoprawny znak rzymski: {znak}")

    wartosc = 0
    i = 0
    while i < len(rzymskie):
        if i + 1 < len(rzymskie) and symbole[rzymskie[i]] < symbole[rzymskie[i+1]]:
            # niepoprawne kombinacje typu IM, XM, VX itp.
            if not poprawna_substrakcja(rzymskie[i], rzymskie[i+1]):
                raise ValueError(f"Niepoprawna notacja rzymska: {rzymskie}")

            wartosc += symbole[rzymskie[i+1]] - symbole[rzymskie[i]]
            i += 2
        else:
            wartosc += symbole[rzymskie[i]]
            i += 1

    if not (1 <= wartosc <= 3999):
        raise ValueError("Liczba musi być w zakresie 1–3999.")

    return wartosc

def poprawna_substrakcja(a, b):
    dozwolone = {
        'I': ['V', 'X'],
        'X': ['L', 'C'],
        'C': ['D', 'M']
    }
    return a in dozwolone and b in dozwolone[a]

def arabskie_na_rzymskie(arabskie):
    if not isinstance(arabskie, int):
        raise ValueError("Liczba arabska musi być typu int.")

    if not (1 <= arabskie <= 3999):
        raise ValueError("Liczba musi być w zakresie 1–3999.")

    wartosci = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]

    wynik = ""
    for wart, znak in wartosci:
        while arabskie >= wart:
            wynik += znak
            arabskie -= wart

    return wynik



# przykład działania 

if __name__ == "__main__":
    try:
        rzymska = "MCMXCIV"
        print(f"Liczba rzymska {rzymska} to {rzymskie_na_arabskie(rzymska)} w arabskich.")

        arabska = 1994
        print(f"Liczba arabska {arabska} to {arabskie_na_rzymskie(arabska)} w rzymskich.")

    except ValueError as e:
        print(e)
