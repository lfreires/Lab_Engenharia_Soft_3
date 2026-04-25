from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from livraria.domain.models.book import Book
from livraria.domain.models.cart import Cart, CartItem
from livraria.domain.ports.repositories import ICartRepository
from .txt_store import TxtStore


class TxtCartRepository(ICartRepository):
    def __init__(self, data_dir: Path) -> None:
        self._carts = TxtStore(data_dir / "carts.txt")
        self._items = TxtStore(data_dir / "cart_items.txt")

    def create(self) -> Cart:
        cart = Cart(id=str(uuid4()))
        self._carts.append({"id": cart.id})
        return cart

    def find(self, cart_id: str) -> Cart:
        if not any(r["id"] == cart_id for r in self._carts.read_all()):
            raise KeyError(f"Carrinho '{cart_id}' não encontrado.")
        items = [
            CartItem(
                book_id=r["book_id"],
                title=r["title"],
                quantity=r["quantity"],
                unit_price=r["unit_price"],
            )
            for r in self._items.read_all()
            if r["cart_id"] == cart_id
        ]
        return Cart(id=cart_id, items=items)

    def add_item(self, cart_id: str, book: Book, quantity: int) -> None:
        records = self._items.read_all()
        for r in records:
            if r["cart_id"] == cart_id and r["book_id"] == book.id:
                r["quantity"] += quantity
                r["title"] = book.title
                r["unit_price"] = book.price
                self._items.write_all(records)
                return
        self._items.append({
            "cart_id": cart_id,
            "book_id": book.id,
            "title": book.title,
            "quantity": quantity,
            "unit_price": book.price,
        })

    def remove_item(self, cart_id: str, book_id: str) -> None:
        records = [
            r for r in self._items.read_all()
            if not (r["cart_id"] == cart_id and r["book_id"] == book_id)
        ]
        self._items.write_all(records)

    def clear(self, cart_id: str) -> None:
        records = [r for r in self._items.read_all() if r["cart_id"] != cart_id]
        self._items.write_all(records)
