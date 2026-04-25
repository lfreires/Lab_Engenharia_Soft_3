from __future__ import annotations

from dataclasses import dataclass

VALID_METHODS = frozenset({"pix", "card", "cash"})


@dataclass
class Payment:
    order_id: str
    amount: float
    method: str
    status: str

    @staticmethod
    def validate(amount: float, method: str) -> None:
        if amount <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")
        if method not in VALID_METHODS:
            raise ValueError("Método de pagamento inválido.")
