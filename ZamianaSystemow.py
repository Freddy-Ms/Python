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
        wynik = iterator = 0
        cyf = [10,11,12,13,14,15]
        lit = ['A', 'B', 'C','D','E','F']
        
        for i in reprezentacja[::-1]:
            if i in lit:
                help = lit.index(i)
                wynik += cyf[help] * pow(system,iterator)
            else:
                wynik += int(i) * pow(system,iterator)
            iterator +=1
        return wynik

print(dziesietnyna(155,16))
print(sysnadziesietny(dziesietnyna(155,16),16))