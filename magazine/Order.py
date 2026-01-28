from __future__ import annotations

from typing import List

import magazine.utils as utils
from magazine.Product import Product


class Order:
    def __init__(self, products: List[Product]) -> None:
        self.order_id = utils.generate_id("ORD")
        self.products = products

    def __str__(self) -> str:
        products_str = ", ".join(p.name for p in self.products)
        return f"Order(id={self.order_id}, products=[{products_str}])"
