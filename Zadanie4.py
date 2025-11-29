def wyswietl_co_drugi(liczby):
    for i in range(0, len(liczby), 2):
        print(liczby[i])

lista = list(range(10))
wyswietl_co_drugi(lista)