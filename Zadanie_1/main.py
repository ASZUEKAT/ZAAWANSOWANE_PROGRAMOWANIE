from __future__ import annotations

from magazine import Product


def main() -> None:
    p1 = Product.Product("Książka", 49.99)
    print(p1)


if __name__ == "__main__":
    main()