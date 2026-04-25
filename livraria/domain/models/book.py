from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Book:
    id: str
    title: str
    price: float
    stock: int

    def can_reserve(self, quantity: int) -> bool:
        if quantity <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return self.stock >= quantity
