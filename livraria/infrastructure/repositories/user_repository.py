from __future__ import annotations

import sqlite3


class UserRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def find(self, username: str) -> tuple[str, str] | None:
        row = self._conn.execute(
            "SELECT username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return (row["username"], row["password_hash"]) if row else None

    def exists(self, username: str) -> bool:
        return self._conn.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone() is not None

    def save(self, username: str, password_hash: str) -> None:
        self._conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        self._conn.commit()
