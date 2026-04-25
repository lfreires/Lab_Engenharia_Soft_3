from __future__ import annotations

from abc import ABC, abstractmethod

from livraria.domain.models.book import Book
from livraria.domain.models.cart import Cart
from livraria.domain.models.coupon import Coupon
from livraria.domain.models.order import Order, OrderItem
from livraria.domain.models.payment import Payment


class IUserRepository(ABC):
    @abstractmethod
    def find(self, username: str) -> tuple[str, str] | None: ...

    @abstractmethod
    def exists(self, username: str) -> bool: ...

    @abstractmethod
    def save(self, username: str, password_hash: str) -> None: ...


class IBookRepository(ABC):
    @abstractmethod
    def find(self, book_id: str) -> Book: ...

    @abstractmethod
    def all(self) -> list[Book]: ...

    @abstractmethod
    def save(self, book: Book) -> None: ...

    @abstractmethod
    def reserve_stock(self, book_id: str, quantity: int) -> None: ...


class ICartRepository(ABC):
    @abstractmethod
    def create(self) -> Cart: ...

    @abstractmethod
    def find(self, cart_id: str) -> Cart: ...

    @abstractmethod
    def add_item(self, cart_id: str, book: Book, quantity: int) -> None: ...

    @abstractmethod
    def remove_item(self, cart_id: str, book_id: str) -> None: ...

    @abstractmethod
    def clear(self, cart_id: str) -> None: ...


class IOrderRepository(ABC):
    @abstractmethod
    def save(
        self,
        order_id: str,
        total: float,
        status: str,
        coupon_code: str | None = None,
    ) -> None: ...

    @abstractmethod
    def save_items(self, order_id: str, items: list[OrderItem]) -> None: ...

    @abstractmethod
    def all(self) -> list[Order]: ...


class IPaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment) -> None: ...


class ICouponRepository(ABC):
    @abstractmethod
    def find(self, code: str) -> Coupon | None: ...

    @abstractmethod
    def save(self, coupon: Coupon) -> None: ...

    @abstractmethod
    def mark_used(self, code: str) -> None: ...
