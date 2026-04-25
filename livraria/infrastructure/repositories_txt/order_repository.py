from __future__ import annotations

from pathlib import Path

from livraria.domain.models.order import Order, OrderItem
from livraria.domain.models.payment import Payment
from livraria.domain.ports.repositories import IOrderRepository
from .txt_store import TxtStore


class TxtOrderRepository(IOrderRepository):
    def __init__(self, data_dir: Path) -> None:
        self._orders = TxtStore(data_dir / "orders.txt")
        self._items = TxtStore(data_dir / "order_items.txt")
        self._payments = TxtStore(data_dir / "payments.txt")

    def save(
        self,
        order_id: str,
        total: float,
        status: str,
        coupon_code: str | None = None,
    ) -> None:
        self._orders.append({
            "id": order_id,
            "total": total,
            "status": status,
            "coupon_code": coupon_code,
        })

    def save_items(self, order_id: str, items: list[OrderItem]) -> None:
        for item in items:
            self._items.append({
                "order_id": order_id,
                "book_id": item.book_id,
                "title": item.title,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            })

    def all(self) -> list[Order]:
        payments_by_order = {
            r["order_id"]: Payment(**r)
            for r in self._payments.read_all()
        }
        all_items = self._items.read_all()
        orders: list[Order] = []
        for r in self._orders.read_all():
            payment = payments_by_order.get(r["id"])
            if payment is None:
                continue
            items = [
                OrderItem(
                    book_id=i["book_id"],
                    title=i["title"],
                    quantity=i["quantity"],
                    unit_price=i["unit_price"],
                )
                for i in all_items
                if i["order_id"] == r["id"]
            ]
            orders.append(Order(
                id=r["id"],
                items=items,
                total=r["total"],
                payment=payment,
                status=r["status"],
                coupon_code=r.get("coupon_code"),
            ))
        return orders
