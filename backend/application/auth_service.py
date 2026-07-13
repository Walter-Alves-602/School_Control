"""
Casos de uso de autenticação: login (emite token) e resolução do usuário
autenticado a partir de um token.
"""

from domain.entities import User
from domain.errors import ForbiddenCargoError, InvalidCredentialsError, InvalidTokenError
from domain.ports import PasswordHasher, TokenService, UserRepository


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        allowed_cargo: str,
        access_token_expire_minutes: int,
    ):
        self._users = user_repository
        self._hasher = password_hasher
        self._tokens = token_service
        self._allowed_cargo = allowed_cargo
        self._expire_minutes = access_token_expire_minutes

    def authenticate(self, login: str, password: str) -> str:
        user = self._users.get_by_login(login)

        if not user or not user.is_active or not self._hasher.verify(password, user.password_hash):
            raise InvalidCredentialsError()

        self.ensure_authorized(user)

        return self._tokens.create_access_token(
            {"sub": user.login, "cargo": user.cargo}, self._expire_minutes
        )

    def get_current_user(self, token: str) -> User:
        payload = self._tokens.decode(token)
        login = payload.get("sub")
        if login is None:
            raise InvalidTokenError()

        user = self._users.get_by_login(login)
        if user is None or not user.is_active:
            raise InvalidTokenError()

        return user

    def ensure_authorized(self, user: User) -> None:
        if user.cargo.upper() != self._allowed_cargo.upper():
            raise ForbiddenCargoError(self._allowed_cargo)
