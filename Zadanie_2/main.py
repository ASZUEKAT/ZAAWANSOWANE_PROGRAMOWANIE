from __future__ import annotations
from datetime import date
from typing import List


class Student:
    def __init__(self, name: str, marks: List[float]) -> None:
        self.name = name
        self.marks = marks

    def __str__(self) -> str:
        avg = (sum(self.marks) / len(self.marks)) if self.marks else 0
        return f"Student(name={self.name}, avg={avg:.2f})"


class Library:
    def __init__(
        self, city: str, street: str, zip_code: str, open_hours: str, phone: str
    ) -> None:
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self) -> str:
        return (
            "Library("
            f"city={self.city}, street={self.street}, zip_code={self.zip_code}, "
            f"open_hours={self.open_hours}, phone={self.phone}"
            ")"
        )


class Employee:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        hire_date: date,
        birth_date: date,
        city: str,
        street: str,
        zip_code: str,
        phone: str,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self) -> str:
        return (
            "Employee("
            f"{self.first_name} {self.last_name}, hire_date={self.hire_date.isoformat()}, "
            f"birth_date={self.birth_date.isoformat()}, address={self.city}, {self.street}, {self.zip_code}, "
            f"phone={self.phone}"
            ")"
        )


class Book:
    def __init__(
        self,
        library: Library,
        publication_date: date,
        author_name: str,
        author_surname: str,
        number_of_pages: int,
    ) -> None:
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self) -> str:
        return (
            "Book("
            f"author={self.author_name} {self.author_surname}, publication_date={self.publication_date.isoformat()}, "
            f"pages={self.number_of_pages}, library={self.library}"
            ")"
        )


class Order:
    def __init__(
        self, employee: Employee, student: Student, books: List[Book], order_date: date
    ) -> None:
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self) -> str:
        books_str = (
            "\n    ".join(str(b) for b in self.books)
            if self.books
            else "(brak książek)"
        )
        return (
            "Order(\n"
            f"  order_date={self.order_date.isoformat()},\n"
            f"  employee={self.employee},\n"
            f"  student={self.student},\n"
            f"  books=[\n"
            f"    {books_str}\n"
            f"  ]\n"
            ")"
        )


def main() -> None:
    # 2 biblioteki
    lib1 = Library(
        "Warszawa", "Marszałkowska 10", "00-001", "08:00-18:00", "+48 111 222 333"
    )
    lib2 = Library("Kraków", "Długa 5", "30-002", "09:00-17:00", "+48 444 555 666")

    # 5 książek
    b1 = Book(lib1, date(2012, 5, 10), "Adam", "Mickiewicz", 350)
    b2 = Book(lib1, date(2018, 1, 20), "Henryk", "Sienkiewicz", 420)
    b3 = Book(lib2, date(2005, 9, 1), "Olga", "Tokarczuk", 280)
    b4 = Book(lib2, date(2020, 11, 15), "Stanisław", "Lem", 310)
    b5 = Book(lib1, date(1999, 6, 30), "Bolesław", "Prus", 510)

    # 3 pracowników
    e1 = Employee(
        "Maria",
        "Lis",
        date(2021, 3, 1),
        date(1990, 7, 12),
        "Warszawa",
        "Marszałkowska 10",
        "00-001",
        "+48 700 100 200",
    )
    e2 = Employee(
        "Piotr",
        "Zieliński",
        date(2019, 10, 5),
        date(1985, 2, 3),
        "Kraków",
        "Długa 5",
        "30-002",
        "+48 700 300 400",
    )
    e3 = Employee(
        "Katarzyna",
        "Wójcik",
        date(2023, 6, 15),
        date(1995, 12, 25),
        "Warszawa",
        "Marszałkowska 10",
        "00-001",
        "+48 700 500 600",
    )

    # 3 studentów
    s1 = Student("Tomasz Student", [55, 60, 70])
    s2 = Student("Alicja Student", [20, 35, 40])
    s3 = Student("Michał Student", [80, 90, 75])

    # 2 zamówienia
    order1 = Order(e1, s1, [b1, b3, b5], date(2026, 1, 20))
    order2 = Order(e2, s3, [b2, b4], date(2026, 1, 27))

    # Wyświetlić oba zamówienia
    print(order1)
    print()
    print(order2)


if __name__ == "__main__":
    main()
