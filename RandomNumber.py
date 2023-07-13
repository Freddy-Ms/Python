import random
print("Gra polega na odgadnieciu losowo wygenerowanej liczbie!")
begin = int(input("Podaj poczatkowy zakres, z ktorego wylosuje liczbe: "))
end = int(input("Podaj koncowy zakres, z ktorego wylosuje liczbe: "))
random = random.randint(begin,end)
counter = 1
guess = end + 1
while guess != random:
    guess = int(input("Zgadnij liczbe: "))
    if guess> end or guess < begin:
        print('Podajesz liczby spoza zakresu')
        counter -= 1
    counter += 1
    print("Sprobuj jeszcze raz!")
print("Gratulacje udalo Ci sie po",str(guess),"probach!")