"""
Gerenciamento de usuários do sistema. Restrito a usuários do cargo TI.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.database import get_db
from auth.deps import require_ti
from auth.models import User
from auth.schemas import UserCreate, UserOut
from auth.security import hash_password

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_ti)])


@router.get("", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login == payload.login).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login já cadastrado")

    user = User(
        name=payload.name,
        login=payload.login,
        password_hash=hash_password(payload.password),
        cargo=payload.cargo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_ti)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if user.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Não é possível remover o próprio usuário")

    db.delete(user)
    db.commit()
