from __future__ import annotations

from Zadanie_2.models.property_base import Property


class House(Property):
    def __init__(self, area: float, rooms: int, price: float, address: str, plot: int) -> None:
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self) -> str:
        return (
            "House("
            f"area={self.area}m2, rooms={self.rooms}, price={self.price} PLN, "
            f"address={self.address}, plot={self.plot}m2"
            ")"
        )
