from __future__ import annotations

from pathlib import Path

from livraria.domain.ports.unit_of_work import IUnitOfWork


class TxtUnitOfWork(IUnitOfWork):
    _FILES = [
        "users.txt",
        "books.txt",
        "carts.txt",
        "cart_items.txt",
        "coupons.txt",
        "orders.txt",
        "order_items.txt",
        "payments.txt",
    ]

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir
        self._snapshots: dict[str, str] = {}

    def begin(self) -> None:
        self._snapshots = {
            name: (self._data_dir / name).read_text(encoding="utf-8")
            if (self._data_dir / name).exists()
            else ""
            for name in self._FILES
        }

    def commit(self) -> None:
        self._snapshots = {}

    def rollback(self) -> None:
        for name, content in self._snapshots.items():
            (self._data_dir / name).write_text(content, encoding="utf-8")
        self._snapshots = {}
