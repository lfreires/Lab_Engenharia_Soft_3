from __future__ import annotations

from dataclasses import dataclass

from livraria.domain.models.payment import Payment


@dataclass
class OrderItem:
    book_id: str
    title: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    id: str
    items: list[OrderItem]
    total: float
    payment: Payment
    status: str
    coupon_code: str | None = None
