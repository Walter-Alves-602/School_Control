"""
Schemas Pydantic (request/response) da API.
"""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


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


class InstallPackageRequest(BaseModel):
    package: str


class CustomCommandRequest(BaseModel):
    command: str
    use_sudo: bool = False
