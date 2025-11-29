def polacz_przetworz(lista1: list, lista2: list) -> list:
    polaczona = lista1 + lista2
    bez_duplikatow = list(set(polaczona))
    wynik = [x ** 3 for x in bez_duplikatow]
    return wynik


print(polacz_przetworz([1, 2, 3], [2, 3, 4]))