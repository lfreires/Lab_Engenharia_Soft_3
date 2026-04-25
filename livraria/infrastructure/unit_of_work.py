from __future__ import annotations

import sqlite3


class UnitOfWork:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def begin(self) -> None:
        self._conn.execute("BEGIN")

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()
