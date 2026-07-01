"""
Schemas Pydantic usados pela API para autenticação e gerenciamento de usuários.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    login: str
    password: str
    cargo: str = "TI"


class UserOut(BaseModel):
    id: int
    name: str
    login: str
    cargo: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
