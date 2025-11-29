def wyswietl_parzyste(liczby):
    for liczba in liczby:
        if liczba % 2 == 0:
            print(liczba)

lista = list(range(10))  
wyswietl_parzyste(lista)