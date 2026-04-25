from __future__ import annotations

import sqlite3
from uuid import uuid4

from livraria.domain.models.book import Book
from livraria.domain.models.cart import Cart, CartItem


class CartRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def create(self) -> Cart:
        cart = Cart(id=str(uuid4()))
        self._conn.execute("INSERT INTO carts (id) VALUES (?)", (cart.id,))
        self._conn.commit()
        return cart

    def find(self, cart_id: str) -> Cart:
        cart_row = self._conn.execute(
            "SELECT id FROM carts WHERE id = ?", (cart_id,)
        ).fetchone()
        if cart_row is None:
            raise KeyError(f"Carrinho '{cart_id}' não encontrado.")
        item_rows = self._conn.execute(
            """
            SELECT book_id, title, quantity, unit_price
            FROM cart_items WHERE cart_id = ? ORDER BY rowid
            """,
            (cart_id,),
        ).fetchall()
        items = [
            CartItem(
                book_id=row["book_id"],
                title=row["title"],
                quantity=row["quantity"],
                unit_price=row["unit_price"],
            )
            for row in item_rows
        ]
        return Cart(id=cart_id, items=items)

    def add_item(self, cart_id: str, book: Book, quantity: int) -> None:
        self._conn.execute(
            """
            INSERT INTO cart_items (cart_id, book_id, title, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(cart_id, book_id) DO UPDATE SET
                title = excluded.title,
                unit_price = excluded.unit_price,
                quantity = cart_items.quantity + excluded.quantity
            """,
            (cart_id, book.id, book.title, quantity, book.price),
        )
        self._conn.commit()

    def remove_item(self, cart_id: str, book_id: str) -> None:
        self._conn.execute(
            "DELETE FROM cart_items WHERE cart_id = ? AND book_id = ?",
            (cart_id, book_id),
        )
        self._conn.commit()

    def clear(self, cart_id: str, commit: bool = True) -> None:
        self._conn.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
        if commit:
            self._conn.commit()
