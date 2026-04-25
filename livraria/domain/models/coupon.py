from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Coupon:
    code: str
    discount_pct: float
    active: bool
    single_use: bool
    used: bool

    def validate(self) -> None:
        if not self.active:
            raise ValueError(f"Cupom '{self.code}' não está ativo.")
        if self.single_use and self.used:
            raise ValueError(f"Cupom '{self.code}' já foi utilizado.")

    def apply(self, total: float) -> float:
        return round(total * (1 - self.discount_pct / 100), 2)
