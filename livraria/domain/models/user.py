from __future__ import annotations

from hashlib import sha256


class User:
    @staticmethod
    def validate(username: str, password: str) -> None:
        if not username or not password:
            raise ValueError("Usuário e senha são obrigatórios.")
        if len(password) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")

    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode("utf-8")).hexdigest()
