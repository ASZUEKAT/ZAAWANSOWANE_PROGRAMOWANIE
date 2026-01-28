from __future__ import annotations

from datetime import date

from Zadanie_2.models.library import Library


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
            f"author={self.author_name} {self.author_surname}, "
            f"publication_date={self.publication_date.isoformat()}, pages={self.number_of_pages}, "
            f"library={self.library}"
            ")"
        )
