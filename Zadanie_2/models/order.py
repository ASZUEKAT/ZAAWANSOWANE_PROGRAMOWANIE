from __future__ import annotations

from datetime import date
from typing import List

from Zadanie_2.models.book import Book
from Zadanie_2.models.employee import Employee
from Zadanie_2.models.student import Student


class Order:
    def __init__(
        self,
        employee: Employee,
        student: Student,
        books: List[Book],
        order_date: date,
    ) -> None:
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self) -> str:
        books_str = "\n    ".join(str(b) for b in self.books) if self.books else "(brak książek)"
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
