"""
Rotas de autenticação: login (emite token JWT) e consulta do usuário logado.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.database import get_db
from auth.deps import get_current_user
from auth.models import User
from auth.schemas import Token, UserOut
from auth.security import create_access_token, verify_password
from config import ALLOWED_CARGO

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == form_data.username).first()

    if not user or not user.is_active or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.cargo.upper() != ALLOWED_CARGO.upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acesso restrito a usuários do cargo '{ALLOWED_CARGO}'",
        )

    token = create_access_token({"sub": user.login, "cargo": user.cargo})
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
