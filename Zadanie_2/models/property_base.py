from __future__ import annotations


class Property:
    def __init__(self, area: float, rooms: int, price: float, address: str) -> None:
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address

    def __str__(self) -> str:
        return (
            "Property("
            f"area={self.area}m2, rooms={self.rooms}, price={self.price} PLN, address={self.address}"
            ")"
        )
