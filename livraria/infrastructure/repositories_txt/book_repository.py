from __future__ import annotations

from pathlib import Path

from livraria.domain.models.book import Book
from livraria.domain.ports.repositories import IBookRepository
from .txt_store import TxtStore


class TxtBookRepository(IBookRepository):
    def __init__(self, data_dir: Path) -> None:
        self._store = TxtStore(data_dir / "books.txt")

    def find(self, book_id: str) -> Book:
        for r in self._store.read_all():
            if r["id"] == book_id:
                return Book(**r)
        raise KeyError(f"Livro '{book_id}' não encontrado.")

    def all(self) -> list[Book]:
        books = [Book(**r) for r in self._store.read_all()]
        return sorted(books, key=lambda b: b.title)

    def save(self, book: Book) -> None:
        if book.stock < 0:
            raise ValueError("O estoque não pode ser negativo.")
        records = self._store.read_all()
        record = {"id": book.id, "title": book.title, "price": book.price, "stock": book.stock}
        for i, r in enumerate(records):
            if r["id"] == book.id:
                records[i] = record
                self._store.write_all(records)
                return
        self._store.append(record)

    def reserve_stock(self, book_id: str, quantity: int) -> None:
        records = self._store.read_all()
        for r in records:
            if r["id"] == book_id:
                if r["stock"] < quantity:
                    raise ValueError(f"Estoque insuficiente para o livro '{book_id}'.")
                r["stock"] -= quantity
                self._store.write_all(records)
                return
        raise KeyError(f"Livro '{book_id}' não encontrado.")
