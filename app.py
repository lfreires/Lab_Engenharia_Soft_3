import os
from pathlib import Path

from livraria.application.services.auth_service import AuthService
from livraria.application.services.book_service import BookService
from livraria.application.services.cart_service import CartService
from livraria.application.services.checkout_service import CheckoutService
from livraria.controllers import AuthController, BookController, CartController, OrderController
from livraria.domain.models.coupon import Coupon
from livraria.infrastructure.repositories_txt.book_repository import TxtBookRepository
from livraria.infrastructure.repositories_txt.cart_repository import TxtCartRepository
from livraria.infrastructure.repositories_txt.coupon_repository import TxtCouponRepository
from livraria.infrastructure.repositories_txt.order_repository import TxtOrderRepository
from livraria.infrastructure.repositories_txt.payment_repository import TxtPaymentRepository
from livraria.infrastructure.repositories_txt.user_repository import TxtUserRepository
from livraria.infrastructure.unit_of_work_txt import TxtUnitOfWork
from livraria.views.tk_view import TkApp

DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "data"


def _seed(auth_svc: AuthService, book_svc: BookService, coupon_repo: TxtCouponRepository) -> None:
    if not auth_svc.exists("admin"):
        auth_svc.register("admin", "123456")
    try:
        book_svc.get_stock("livro-001")
    except KeyError:
        book_svc.create("Engenharia de Software na Pratica", 89.90, 10, book_id="livro-001")
    if coupon_repo.find("DESC10") is None:
        coupon_repo.save(Coupon(code="DESC10", discount_pct=10.0, active=True, single_use=False, used=False))


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    user_repo    = TxtUserRepository(DATA_DIR)
    book_repo    = TxtBookRepository(DATA_DIR)
    cart_repo    = TxtCartRepository(DATA_DIR)
    order_repo   = TxtOrderRepository(DATA_DIR)
    payment_repo = TxtPaymentRepository(DATA_DIR)
    coupon_repo  = TxtCouponRepository(DATA_DIR)
    uow          = TxtUnitOfWork(DATA_DIR)

    auth_svc     = AuthService(user_repo)
    book_svc     = BookService(book_repo)
    cart_svc     = CartService(cart_repo, book_repo)
    checkout_svc = CheckoutService(book_repo, cart_repo, order_repo, payment_repo, coupon_repo, uow)

    _seed(auth_svc, book_svc, coupon_repo)

    auth_ctrl  = AuthController(auth_svc)
    book_ctrl  = BookController(book_svc)
    cart_ctrl  = CartController(cart_svc)
    order_ctrl = OrderController(checkout_svc)

    app = TkApp(auth_ctrl, book_ctrl, cart_ctrl, order_ctrl)
    app.run()


if __name__ == "__main__":
    main()
