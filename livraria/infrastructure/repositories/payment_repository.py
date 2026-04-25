from __future__ import annotations

import sqlite3

from livraria.domain.models.payment import Payment


class PaymentRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def save(self, payment: Payment, commit: bool = True) -> None:
        self._conn.execute(
            """
            INSERT INTO payments (order_id, amount, method, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(order_id) DO UPDATE SET
                amount = excluded.amount,
                method = excluded.method,
                status = excluded.status
            """,
            (payment.order_id, payment.amount, payment.method, payment.status),
        )
        if commit:
            self._conn.commit()
