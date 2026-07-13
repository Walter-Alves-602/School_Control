"""
Portas (interfaces) que o domínio/aplicação espera da infraestrutura.
Cada porta tem um adapter concreto em backend/adapters/.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from domain.entities import Computador, Sala, User

# (ip, sucesso, saida/erro)
CommandResult = Tuple[str, bool, str]


class UserRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[User]: ...

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def add(self, user: User) -> User: ...

    @abstractmethod
    def update_password(self, user: User, password_hash: str) -> None: ...

    @abstractmethod
    def delete(self, user: User) -> None: ...


class ComputerRepository(ABC):
    @abstractmethod
    def load_all(self) -> List[Computador]: ...

    @abstractmethod
    def get_by_sala(self, sala_name: str) -> List[Computador]: ...

    @abstractmethod
    def list_salas_summary(self) -> Dict[str, int]: ...

    @abstractmethod
    def get_available_salas(self) -> List[str]: ...

    @abstractmethod
    def get_sala_config(self, sala_name: str) -> Sala: ...

    @abstractmethod
    def get_command_for_sala(self, sala_name: str, command_type: str, **kwargs) -> str: ...


class RemoteExecutor(ABC):
    @abstractmethod
    def run(
        self,
        command: str,
        hosts: List[str],
        username: str,
        password: str,
        port: int,
        timeout: int,
        use_sudo: bool = False,
    ) -> List[CommandResult]: ...

    @abstractmethod
    def test_connectivity(
        self,
        hosts: List[str],
        username: str,
        password: str,
        port: int,
        timeout: int,
    ) -> Dict[str, bool]: ...


class WakeOnLanSender(ABC):
    @abstractmethod
    def send(self, mac_address: str, broadcast_ip: str) -> bool: ...


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool: ...


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, data: dict, expires_minutes: int) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> dict: ...
