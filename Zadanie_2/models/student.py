from __future__ import annotations

from typing import List


class Student:
    def __init__(self, name: str, marks: List[float]) -> None:
        self.name = name
        self.marks = marks

    def is_passed(self) -> bool:
        if not self.marks:
            return False
        return (sum(self.marks) / len(self.marks)) > 50

    def __str__(self) -> str:
        avg = (sum(self.marks) / len(self.marks)) if self.marks else 0
        return f"Student(name={self.name}, avg={avg:.2f}, passed={self.is_passed()})"
