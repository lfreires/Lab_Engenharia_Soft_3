from livraria.domain.models.book import Book
from livraria.domain.models.order import Order


class ConsoleView:
    def show_login_success(self, username: str) -> None:
        print(f"Login realizado com sucesso para o usuário '{username}'.")

    def show_login_failure(self) -> None:
        print("Falha na autenticação do usuário.")

    def show_book_created(self, book: Book) -> None:
        print(f"Livro criado: {book.title} (id={book.id}, estoque={book.stock})")

    def show_order_created(self, order: Order) -> None:
        print(f"Pedido criado: {order.id}")
        print(f"Total: R$ {order.total:.2f}")
        print(f"Pagamento: {order.payment.method} - {order.payment.status}")

    def show_remaining_stock(self, title: str, stock: int) -> None:
        print(f"Estoque restante de '{title}': {stock}")
