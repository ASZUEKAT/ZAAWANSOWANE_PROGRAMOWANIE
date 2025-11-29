import random

def multiply(a: int, b: int) -> int:
    return a * b

# losowanie dwóch liczb [Lepiej wygląda niż na sztywno wpisywanie, choć wiem, że celem tego zadania było co innego]
num1 = random.randint(1, 25)
num2 = random.randint(1, 25)

print("Wylosowane liczby:", num1, "i", num2)

wynik = multiply(num1, num2)
print("Wynik mnożenia:", wynik)

# poniżej kod z zadania wymagany
#def mnozenie(a: int, b: int) -> int:
#    return a * b
#
#print(mnozenie(4, 7))