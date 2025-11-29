def pomnoz_przez_dwa_for(liczby):
    wynik = []
    for liczba in liczby:
        wynik.append(liczba * 2)
    return wynik

lista = [1, 2, 3, 4, 5]
print(pomnoz_przez_dwa_for(lista))

def pomnoz_przez_dwa_lista_skladana(liczby):
    return [liczba * 2 for liczba in liczby]

lista = [1, 2, 3, 4, 5]
print(pomnoz_przez_dwa_lista_skladana(lista))