from __future__ import annotations

import magazine.utils as utils


class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price
        self.product_id = utils.generate_id("PROD")

    def __str__(self) -> str:
        return (
            "Product("
            f"id={self.product_id}, name={self.name}, price={utils.format_price(self.price)}"
            ")"
        )
