from __future__ import annotations
from datetime import date
from typing import List


class Student:
    def __init__(self, name: str, marks: List[float]) -> None:
        self.name = name
        self.marks = marks

    def is_passed(self) -> bool:
        if not self.marks:
            return False
        avg = sum(self.marks) / len(self.marks)
        return avg > 50

    def __str__(self) -> str:
        avg = (sum(self.marks) / len(self.marks)) if self.marks else 0
        return f"Student(name={self.name}, marks={self.marks}, avg={avg:.2f}, passed={self.is_passed()})"


s1 = Student("Anna", [60, 70, 55])
s2 = Student("Jan", [40, 45, 50])

print(s1.is_passed())  # True
print(s2.is_passed())  # False
