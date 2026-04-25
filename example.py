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
from livraria.views import ConsoleView

DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "data"


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    view = ConsoleView()

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

    auth_ctrl  = AuthController(auth_svc)
    book_ctrl  = BookController(book_svc)
    cart_ctrl  = CartController(cart_svc)
    order_ctrl = OrderController(checkout_svc)

    if not auth_ctrl.user_exists("admin"):
        auth_ctrl.register_user("admin", "123456")
    if coupon_repo.find("DESC10") is None:
        coupon_repo.save(Coupon(code="DESC10", discount_pct=10.0, active=True, single_use=False, used=False))

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


if __name__ == "__main__":
    main()
