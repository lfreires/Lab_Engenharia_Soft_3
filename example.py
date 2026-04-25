import os

from livraria.application.services.auth_service import AuthService
from livraria.application.services.book_service import BookService
from livraria.application.services.cart_service import CartService
from livraria.application.services.checkout_service import CheckoutService
from livraria.controllers import AuthController, BookController, CartController, OrderController
from livraria.database import get_connection, init_db
from livraria.infrastructure.repositories.book_repository import BookRepository
from livraria.infrastructure.repositories.cart_repository import CartRepository
from livraria.infrastructure.repositories.coupon_repository import CouponRepository
from livraria.infrastructure.repositories.order_repository import OrderRepository
from livraria.infrastructure.repositories.payment_repository import PaymentRepository
from livraria.infrastructure.repositories.user_repository import UserRepository
from livraria.infrastructure.unit_of_work import UnitOfWork
from livraria.views import ConsoleView

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "livraria.db")


def main() -> None:
    connection = get_connection(DB_PATH)
    try:
        init_db(connection)

        view = ConsoleView()

        user_repo = UserRepository(connection)
        book_repo = BookRepository(connection)
        cart_repo = CartRepository(connection)
        order_repo = OrderRepository(connection)
        payment_repo = PaymentRepository(connection)
        coupon_repo = CouponRepository(connection)

        uow = UnitOfWork(connection)

        auth_svc = AuthService(user_repo)
        book_svc = BookService(book_repo)
        cart_svc = CartService(cart_repo, book_repo)
        checkout_svc = CheckoutService(book_repo, cart_repo, order_repo, payment_repo, coupon_repo, uow)

        auth_ctrl = AuthController(auth_svc)
        book_ctrl = BookController(book_svc)
        cart_ctrl = CartController(cart_svc)
        order_ctrl = OrderController(checkout_svc)

        if not auth_ctrl.user_exists("admin"):
            auth_ctrl.register_user("admin", "123456")
        if not auth_ctrl.login("admin", "123456"):
            view.show_login_failure()
            raise PermissionError("Falha na autenticação do usuário.")
        view.show_login_success("admin")

        book = book_ctrl.create_book(
            title="Engenharia de Software na Pratica",
            price=89.90,
            stock=10,
            book_id="livro-001",
        )
        view.show_book_created(book)

        cart = cart_ctrl.create_cart()
        cart_ctrl.add_book(cart.id, book.id, quantity=2)

        order = order_ctrl.checkout(cart.id, payment_method="pix", coupon_code="DESC10")
        view.show_order_created(order)
        view.show_remaining_stock(book.title, book_ctrl.get_stock(book.id))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
