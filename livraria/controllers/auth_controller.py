from livraria.application.services.auth_service import AuthService


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self._service = service

    def register_user(self, username: str, password: str) -> None:
        self._service.register(username, password)

    def user_exists(self, username: str) -> bool:
        return self._service.exists(username)

    def login(self, username: str, password: str) -> bool:
        return self._service.authenticate(username, password)
