"""
Hash de senhas (bcrypt) e emissão/validação de tokens JWT. Implementa os
ports PasswordHasher e TokenService (domain/ports.py).
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import JWT_ALGORITHM, SECRET_KEY
from domain.errors import InvalidTokenError
from domain.ports import PasswordHasher, TokenService


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


class JwtTokenService(TokenService):
    def create_access_token(self, data: dict, expires_minutes: int) -> str:
        to_encode = data.copy()
        to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError as exc:
            raise InvalidTokenError(str(exc)) from exc
