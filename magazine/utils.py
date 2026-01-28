from __future__ import annotations

from datetime import datetime


def generate_id(prefix: str) -> str:
    """Generate simple unique id based on time."""
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}-{stamp}"


def format_price(value: float) -> str:
    return f"{value:.2f} PLN"
