from __future__ import annotations

import sqlite3

from livraria.domain.models.order import Order, OrderItem
from livraria.domain.models.payment import Payment


class OrderRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def save(self, order_id: str, total: float, status: str, coupon_code: str | None = None) -> None:
        self._conn.execute(
            "INSERT INTO orders (id, total, status, coupon_code) VALUES (?, ?, ?, ?)",
            (order_id, total, status, coupon_code),
        )

    def save_items(self, order_id: str, items: list[OrderItem]) -> None:
        self._conn.executemany(
            """
            INSERT INTO order_items (order_id, book_id, title, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (order_id, item.book_id, item.title, item.quantity, item.unit_price)
                for item in items
            ],
        )

    def all(self) -> list[Order]:
        order_rows = self._conn.execute(
            "SELECT id, total, status, coupon_code FROM orders ORDER BY rowid"
        ).fetchall()
        orders: list[Order] = []
        for order_row in order_rows:
            payment_row = self._conn.execute(
                "SELECT order_id, amount, method, status FROM payments WHERE order_id = ?",
                (order_row["id"],),
            ).fetchone()
            if payment_row is None:
                continue
            item_rows = self._conn.execute(
                """
                SELECT book_id, title, quantity, unit_price
                FROM order_items WHERE order_id = ? ORDER BY rowid
                """,
                (order_row["id"],),
            ).fetchall()
            items = [
                OrderItem(
                    book_id=row["book_id"],
                    title=row["title"],
                    quantity=row["quantity"],
                    unit_price=row["unit_price"],
                )
                for row in item_rows
            ]
            payment = Payment(
                order_id=payment_row["order_id"],
                amount=payment_row["amount"],
                method=payment_row["method"],
                status=payment_row["status"],
            )
            orders.append(
                Order(
                    id=order_row["id"],
                    items=items,
                    total=order_row["total"],
                    payment=payment,
                    status=order_row["status"],
                    coupon_code=order_row["coupon_code"],
                )
            )
        return orders
