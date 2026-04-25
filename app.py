import os

from livraria.application.services.auth_service import AuthService
from livraria.application.services.book_service import BookService
from livraria.application.services.cart_service import CartService
from livraria.application.services.checkout_service import CheckoutService
from livraria.controllers import AuthController, BookController, CartController, OrderController
from livraria.database import get_connection, init_db
from livraria.domain.models.coupon import Coupon
from livraria.infrastructure.repositories.book_repository import BookRepository
from livraria.infrastructure.repositories.cart_repository import CartRepository
from livraria.infrastructure.repositories.coupon_repository import CouponRepository
from livraria.infrastructure.repositories.order_repository import OrderRepository
from livraria.infrastructure.repositories.payment_repository import PaymentRepository
from livraria.infrastructure.repositories.user_repository import UserRepository
from livraria.infrastructure.unit_of_work import UnitOfWork
from livraria.views.tk_view import TkApp

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "livraria.db")


def _seed(auth_svc: AuthService, coupon_repo: CouponRepository) -> None:
    if not auth_svc.exists("admin"):
        auth_svc.register("admin", "123456")
    if coupon_repo.find("DESC10") is None:
        coupon_repo.save(Coupon(code="DESC10", discount_pct=10.0, active=True, single_use=False, used=False))


def main() -> None:
    connection = get_connection(DB_PATH)
    init_db(connection)

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

    _seed(auth_svc, coupon_repo)

    auth_ctrl = AuthController(auth_svc)
    book_ctrl = BookController(book_svc)
    cart_ctrl = CartController(cart_svc)
    order_ctrl = OrderController(checkout_svc)

    app = TkApp(auth_ctrl, book_ctrl, cart_ctrl, order_ctrl)
    app.run()

    connection.close()


if __name__ == "__main__":
    main()
