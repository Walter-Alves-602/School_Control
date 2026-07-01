"""
Dependências FastAPI para autenticação e controle de acesso.
Apenas usuários com o cargo configurado em ALLOWED_CARGO (padrão: "TI")
podem acessar os recursos protegidos do sistema.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth.database import get_db
from auth.models import User
from auth.security import decode_access_token
from config import ALLOWED_CARGO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        login = payload.get("sub")
        if login is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.login == login).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_ti(current_user: User = Depends(get_current_user)) -> User:
    if current_user.cargo.upper() != ALLOWED_CARGO.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acesso restrito a usuários do cargo '{ALLOWED_CARGO}'",
        )
    return current_user
