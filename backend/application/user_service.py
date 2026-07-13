"""
Casos de uso de gerenciamento de usuários do sistema.
"""

from typing import List

from domain.entities import User
from domain.errors import CannotDeleteSelfError, DuplicateLoginError, UserNotFoundError
from domain.ports import PasswordHasher, UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self._users = user_repository
        self._hasher = password_hasher

    def list_users(self) -> List[User]:
        return self._users.list_all()

    def create_user(self, name: str, login: str, password: str, cargo: str) -> User:
        if self._users.get_by_login(login):
            raise DuplicateLoginError()

        user = User(id=None, name=name, login=login, password_hash=self._hasher.hash(password), cargo=cargo)
        return self._users.add(user)

    def reset_password(self, login: str, new_password: str) -> None:
        user = self._users.get_by_login(login)
        if not user:
            raise UserNotFoundError()

        self._users.update_password(user, self._hasher.hash(new_password))

    def delete_user(self, user_id: int, current_user_id: int) -> None:
        user = self._users.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        if user.id == current_user_id:
            raise CannotDeleteSelfError()

        self._users.delete(user)

    def delete_by_login(self, login: str) -> None:
        user = self._users.get_by_login(login)
        if not user:
            raise UserNotFoundError()

        self._users.delete(user)
