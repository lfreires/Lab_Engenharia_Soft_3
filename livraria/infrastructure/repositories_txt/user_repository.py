from __future__ import annotations

from pathlib import Path

from livraria.domain.ports.repositories import IUserRepository
from .txt_store import TxtStore


class TxtUserRepository(IUserRepository):
    def __init__(self, data_dir: Path) -> None:
        self._store = TxtStore(data_dir / "users.txt")

    def find(self, username: str) -> tuple[str, str] | None:
        for r in self._store.read_all():
            if r["username"] == username:
                return (r["username"], r["password_hash"])
        return None

    def exists(self, username: str) -> bool:
        return self.find(username) is not None

    def save(self, username: str, password_hash: str) -> None:
        records = self._store.read_all()
        for r in records:
            if r["username"] == username:
                r["password_hash"] = password_hash
                self._store.write_all(records)
                return
        self._store.append({"username": username, "password_hash": password_hash})
