from __future__ import annotations

from pathlib import Path

from livraria.domain.models.coupon import Coupon
from livraria.domain.ports.repositories import ICouponRepository
from .txt_store import TxtStore


class TxtCouponRepository(ICouponRepository):
    def __init__(self, data_dir: Path) -> None:
        self._store = TxtStore(data_dir / "coupons.txt")

    def find(self, code: str) -> Coupon | None:
        for r in self._store.read_all():
            if r["code"] == code:
                return Coupon(**r)
        return None

    def save(self, coupon: Coupon) -> None:
        records = self._store.read_all()
        record = {
            "code": coupon.code,
            "discount_pct": coupon.discount_pct,
            "active": coupon.active,
            "single_use": coupon.single_use,
            "used": coupon.used,
        }
        for i, r in enumerate(records):
            if r["code"] == coupon.code:
                records[i] = record
                self._store.write_all(records)
                return
        self._store.append(record)

    def mark_used(self, code: str) -> None:
        records = self._store.read_all()
        for r in records:
            if r["code"] == code:
                r["used"] = True
                self._store.write_all(records)
                return
