from __future__ import annotations


class Property:
    def __init__(self, area: float, rooms: int, price: float, address: str) -> None:
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address

    def __str__(self) -> str:
        return f"Property(area={self.area}m2, rooms={self.rooms}, price={self.price} PLN, address={self.address})"


class House(Property):
    def __init__(
        self, area: float, rooms: int, price: float, address: str, plot: int
    ) -> None:
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self) -> str:
        return (
            "House("
            f"area={self.area}m2, rooms={self.rooms}, price={self.price} PLN, "
            f"address={self.address}, plot={self.plot}m2"
            ")"
        )


class Flat(Property):
    def __init__(
        self, area: float, rooms: int, price: float, address: str, floor: int
    ) -> None:
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self) -> str:
        return (
            "Flat("
            f"area={self.area}m2, rooms={self.rooms}, price={self.price} PLN, "
            f"address={self.address}, floor={self.floor}"
            ")"
        )


def main() -> None:
    house = House(
        area=140.5, rooms=5, price=950_000, address="Warszawa, ul. Lipowa 12", plot=600
    )
    flat = Flat(
        area=52.0, rooms=2, price=520_000, address="Kraków, ul. Kwiatowa 7/12", floor=3
    )

    print(house)
    print(flat)


if __name__ == "__main__":
    main()
