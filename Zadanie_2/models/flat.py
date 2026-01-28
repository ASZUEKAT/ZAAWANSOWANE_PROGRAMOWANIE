from __future__ import annotations

from Zadanie_2.models.property_base import Property


class Flat(Property):
    def __init__(self, area: float, rooms: int, price: float, address: str, floor: int) -> None:
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self) -> str:
        return (
            "Flat("
            f"area={self.area}m2, rooms={self.rooms}, price={self.price} PLN, "
            f"address={self.address}, floor={self.floor}"
            ")"
        )
