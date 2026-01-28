from __future__ import annotations

from datetime import date

from Zadanie_2.models.book import Book
from Zadanie_2.models.employee import Employee
from Zadanie_2.models.flat import Flat
from Zadanie_2.models.house import House
from Zadanie_2.models.library import Library
from Zadanie_2.models.order import Order
from Zadanie_2.models.student import Student


def main() -> None:
    student_ok = Student("Anna Nowak", [60, 70, 55])
    print(student_ok)

    lib1 = Library("Warszawa", "Marszałkowska 10", "00-001", "08:00-18:00", "+48 111 222 333")
    emp1 = Employee(
        "Maria",
        "Lis",
        date(2021, 3, 1),
        date(1990, 7, 12),
        "Warszawa",
        "Marszałkowska 10",
        "00-001",
        "+48 700 100 200",
    )
    b1 = Book(lib1, date(2012, 5, 10), "Adam", "Mickiewicz", 350)
    order = Order(emp1, student_ok, [b1], date.today())
    print(order)

    house = House(140.5, 5, 950_000, "Warszawa, ul. Lipowa 12", 600)
    flat = Flat(52.0, 2, 520_000, "Kraków, ul. Kwiatowa 7/12", 3)
    print(house)
    print(flat)


if __name__ == "__main__":
    main()
