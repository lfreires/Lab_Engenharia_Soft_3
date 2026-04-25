from __future__ import annotations

from livraria.domain.models.cart import Cart
from livraria.infrastructure.repositories.book_repository import BookRepository
from livraria.infrastructure.repositories.cart_repository import CartRepository


class CartService:
    def __init__(self, cart_repo: CartRepository, book_repo: BookRepository) -> None:
        self._cart_repo = cart_repo
        self._book_repo = book_repo

    def create(self) -> Cart:
        return self._cart_repo.create()

    def get(self, cart_id: str) -> Cart:
        return self._cart_repo.find(cart_id)

    def add_book(self, cart_id: str, book_id: str, quantity: int = 1) -> Cart:
        cart = self._cart_repo.find(cart_id)
        book = self._book_repo.find(book_id)
        cart.validate_add(book.id, book.title, book.stock, quantity)
        self._cart_repo.add_item(cart_id, book, quantity)
        return self._cart_repo.find(cart_id)

    def remove_book(self, cart_id: str, book_id: str) -> Cart:
        self._cart_repo.remove_item(cart_id, book_id)
        return self._cart_repo.find(cart_id)
