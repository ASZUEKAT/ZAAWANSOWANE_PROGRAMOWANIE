import random

def czy_parzysta(liczba: int) -> bool:
    return liczba % 2 == 0

los = random.randint(1, 25)
print("Losowana Liczba",los)
wynik = czy_parzysta(los)

if wynik:
    print("Liczba parzysta")
else:
    print("Liczba nieparzysta")