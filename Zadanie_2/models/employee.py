from __future__ import annotations

from datetime import date


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
            f"birth_date={self.birth_date.isoformat()}, "
            f"address={self.city}, {self.street}, {self.zip_code}, phone={self.phone}"
            ")"
        )
