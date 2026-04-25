from livraria.application.services.cart_service import CartService
from livraria.domain.models.cart import Cart


class CartController:
    def __init__(self, service: CartService) -> None:
        self._service = service

    def create_cart(self) -> Cart:
        return self._service.create()

    def get_cart(self, cart_id: str) -> Cart:
        return self._service.get(cart_id)

    def add_book(self, cart_id: str, book_id: str, quantity: int = 1) -> Cart:
        return self._service.add_book(cart_id, book_id, quantity)

    def remove_book(self, cart_id: str, book_id: str) -> Cart:
        return self._service.remove_book(cart_id, book_id)
