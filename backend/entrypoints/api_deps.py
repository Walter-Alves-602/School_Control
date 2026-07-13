"""
Dependências (Depends) do FastAPI: sessão de banco, serviços de aplicação e
autenticação/autorização de rotas. É aqui que os adapters concretos são
instanciados e injetados nos casos de uso (composition root das dependências
por requisição).
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from adapters.csv_repository import CsvComputerRepository
from adapters.db import SqlAlchemyUserRepository, get_db_session
from adapters.security import BcryptPasswordHasher, JwtTokenService
from adapters.ssh_executor import ParamikoRemoteExecutor
from adapters.wol_sender import UdpWakeOnLanSender
from application.auth_service import AuthService
from application.sala_service import SalaService
from application.user_service import UserService
from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALLOWED_CARGO,
    DEFAULT_SSH_TIMEOUT,
    WOL_BROADCAST_IP,
)
from domain.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Adapters sem estado por requisição podem ser compartilhados como singletons.
_password_hasher = BcryptPasswordHasher()
_token_service = JwtTokenService()
_computer_repository = CsvComputerRepository()
_remote_executor = ParamikoRemoteExecutor()
_wol_sender = UdpWakeOnLanSender()


def get_auth_service(db: Session = Depends(get_db_session)) -> AuthService:
    return AuthService(
        user_repository=SqlAlchemyUserRepository(db),
        password_hasher=_password_hasher,
        token_service=_token_service,
        allowed_cargo=ALLOWED_CARGO,
        access_token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def get_user_service(db: Session = Depends(get_db_session)) -> UserService:
    return UserService(user_repository=SqlAlchemyUserRepository(db), password_hasher=_password_hasher)


def get_sala_service() -> SalaService:
    return SalaService(
        computer_repository=_computer_repository,
        remote_executor=_remote_executor,
        wol_sender=_wol_sender,
        wol_broadcast_ip=WOL_BROADCAST_IP,
        default_ssh_timeout=DEFAULT_SSH_TIMEOUT,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    return auth_service.get_current_user(token)


def require_ti(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    auth_service.ensure_authorized(current_user)
    return current_user
