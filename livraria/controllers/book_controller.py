from livraria.application.services.book_service import BookService
from livraria.domain.models.book import Book


class BookController:
    def __init__(self, service: BookService) -> None:
        self._service = service

    def create_book(self, title: str, price: float, stock: int, book_id: str | None = None) -> Book:
        return self._service.create(title, price, stock, book_id)

    def list_books(self) -> list[Book]:
        return self._service.list_all()

    def get_stock(self, book_id: str) -> int:
        return self._service.get_stock(book_id)
