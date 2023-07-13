import math
def dziesietnyna(liczba, system):
    liczba = abs(liczba)
    if system > 16 or system < 0:
        return "Taki system nie istnieje!"
    elif system == 1:
        wynik = ""
        for i in range(liczba):
            wynik += "I"
        return wynik 
    else:
        wynik = ""
        cyf = [10,11,12,13,14,15]
        lit = ['A', 'B', 'C','D','E','F']
        while liczba > 0:
            reszta = liczba % system
            if reszta >= 10:
                indeks = cyf.index(reszta)
                reszta = lit[indeks]
            wynik = str(reszta) + wynik
            liczba //= system 
        return wynik
def sysnadziesietny(reprezentacja, system):
    if system > 16 or system < 0:
        return "Taki system nie istnieje!"
    elif system == 1:
        wynik = len(reprezentacja)
    else:
        reprezentacja = str(reprezentacja)
        dlugosc = len(reprezentacja) - 1
        wynik = iterator = 0
        cyf = [10,11,12,13,14,15]
        lit = ['A', 'B', 'C','D','E','F']
        while dlugosc >= 0:
            if reprezentacja[dlugosc] in lit:
                indeks = lit.index(reprezentacja[dlugosc])
                wynik += cyf[indeks] * pow(system,iterator)
            else:
                wynik += int(reprezentacja[dlugosc]) * pow(system,iterator)
            dlugosc-= 1
            iterator += 1
        return wynik
  

print(dziesietnyna(155,16))
print(sysnadziesietny(dziesietnyna(155,16),16))