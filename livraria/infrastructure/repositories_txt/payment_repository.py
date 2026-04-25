from __future__ import annotations

from pathlib import Path

from livraria.domain.models.payment import Payment
from livraria.domain.ports.repositories import IPaymentRepository
from .txt_store import TxtStore


class TxtPaymentRepository(IPaymentRepository):
    def __init__(self, data_dir: Path) -> None:
        self._store = TxtStore(data_dir / "payments.txt")

    def save(self, payment: Payment) -> None:
        records = self._store.read_all()
        record = {
            "order_id": payment.order_id,
            "amount": payment.amount,
            "method": payment.method,
            "status": payment.status,
        }
        for i, r in enumerate(records):
            if r["order_id"] == payment.order_id:
                records[i] = record
                self._store.write_all(records)
                return
        self._store.append(record)
