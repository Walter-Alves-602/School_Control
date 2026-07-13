"""
Gerenciamento de usuários do sistema. Restrito a usuários do cargo TI.
"""

from typing import List

from fastapi import APIRouter, Depends, status

from application.user_service import UserService
from domain.entities import User
from entrypoints.api_deps import get_current_user, get_user_service, require_ti
from entrypoints.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_ti)])


@router.get("", response_model=List[UserOut])
def list_users(user_service: UserService = Depends(get_user_service)):
    return user_service.list_users()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(payload.name, payload.login, payload.password, payload.cargo)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    user_service.delete_user(user_id, current_user.id)
