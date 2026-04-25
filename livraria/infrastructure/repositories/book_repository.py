from __future__ import annotations

import sqlite3

from livraria.domain.models.book import Book


class BookRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def find(self, book_id: str) -> Book:
        row = self._conn.execute(
            "SELECT id, title, price, stock FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"Livro '{book_id}' não encontrado.")
        return Book(id=row["id"], title=row["title"], price=row["price"], stock=row["stock"])

    def all(self) -> list[Book]:
        rows = self._conn.execute(
            "SELECT id, title, price, stock FROM books ORDER BY title"
        ).fetchall()
        return [Book(id=r["id"], title=r["title"], price=r["price"], stock=r["stock"]) for r in rows]

    def save(self, book: Book) -> None:
        if book.stock < 0:
            raise ValueError("O estoque não pode ser negativo.")
        self._conn.execute(
            """
            INSERT INTO books (id, title, price, stock)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                price = excluded.price,
                stock = excluded.stock
            """,
            (book.id, book.title, book.price, book.stock),
        )
        self._conn.commit()

    def reserve_stock(self, book_id: str, quantity: int, commit: bool = True) -> None:
        cursor = self._conn.execute(
            """
            UPDATE books SET stock = stock - ?
            WHERE id = ? AND stock >= ?
            """,
            (quantity, book_id, quantity),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Estoque insuficiente para o livro '{book_id}'.")
        if commit:
            self._conn.commit()
