from __future__ import annotations

import math
import re
from typing import Any


def is_palindrome(text: str) -> bool:
    """Check if text is a palindrome (ignoring spaces and letter case)."""
    normalized = re.sub(r"\s+", "", text).casefold()
    return normalized == normalized[::-1]


def fibonacci(n: int) -> int:
    """Return n-th Fibonacci number. Assumes fibonacci(0)=0 and fibonacci(1)=1."""
    if n < 0:
        raise ValueError("n must be >= 0")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def count_vowels(text: str) -> int:
    """Count vowels in text (case-insensitive). Includes Polish vowels as well."""
    vowels = set("aeiouyąęó")
    return sum(1 for ch in text.casefold() if ch in vowels)


def calculate_discount(price: float, discount: float) -> float:
    """Return discounted price. Discount must be within [0, 1]."""
    if not (0 <= discount <= 1):
        raise ValueError("discount must be between 0 and 1")
    return price * (1 - discount)


def flatten_list(nested_list: list) -> list:
    """Flatten a list that can contain nested lists."""
    result: list[Any] = []

    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)

    return result


def word_frequencies(text: str) -> dict[str, int]:
    """Return word frequencies (case-insensitive, ignoring punctuation)."""
    words = re.findall(
        r"[0-9A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż]+",
        text.casefold(),
    )
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def is_prime(n: int) -> bool:
    """Check if n is a prime number. If n < 2 returns False."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limit = int(math.isqrt(n))
    for d in range(3, limit + 1, 2):
        if n % d == 0:
            return False
    return True
