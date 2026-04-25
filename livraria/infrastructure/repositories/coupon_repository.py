from __future__ import annotations

import sqlite3

from livraria.domain.models.coupon import Coupon


class CouponRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def find(self, code: str) -> Coupon | None:
        row = self._conn.execute(
            "SELECT code, discount_pct, active, single_use, used FROM coupons WHERE code = ?",
            (code,),
        ).fetchone()
        if row is None:
            return None
        return Coupon(
            code=row["code"],
            discount_pct=row["discount_pct"],
            active=bool(row["active"]),
            single_use=bool(row["single_use"]),
            used=bool(row["used"]),
        )

    def save(self, coupon: Coupon) -> None:
        self._conn.execute(
            """
            INSERT INTO coupons (code, discount_pct, active, single_use, used)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET
                discount_pct = excluded.discount_pct,
                active = excluded.active,
                single_use = excluded.single_use,
                used = excluded.used
            """,
            (
                coupon.code,
                coupon.discount_pct,
                int(coupon.active),
                int(coupon.single_use),
                int(coupon.used),
            ),
        )
        self._conn.commit()

    def mark_used(self, code: str, commit: bool = True) -> None:
        self._conn.execute("UPDATE coupons SET used = 1 WHERE code = ?", (code,))
        if commit:
            self._conn.commit()
