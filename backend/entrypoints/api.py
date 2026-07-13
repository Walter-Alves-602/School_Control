"""
API (FastAPI) do Sistema de Controle de Computadores por Salas.
Executa localmente e é consumida pela interface web (feita separadamente).

Para rodar (a partir da pasta backend/):
    uvicorn entrypoints.api:app --host 0.0.0.0 --port 8000
"""

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from adapters.db import Base, engine
from config import CORS_ORIGINS, SCHOOL_NAME
from domain.errors import (
    CannotDeleteSelfError,
    DuplicateLoginError,
    ForbiddenCargoError,
    InvalidCredentialsError,
    InvalidTokenError,
    SalaNotFoundError,
    UserNotFoundError,
)
from entrypoints.routers import auth_router, salas_router, users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=f"Sistema de Controle de Computadores - {SCHOOL_NAME}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _error_response(status_code: int, detail: str, headers: Optional[dict] = None) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": detail}, headers=headers)


@app.exception_handler(InvalidCredentialsError)
def _invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return _error_response(401, "Login ou senha incorretos", {"WWW-Authenticate": "Bearer"})


@app.exception_handler(InvalidTokenError)
def _invalid_token_handler(request: Request, exc: InvalidTokenError):
    return _error_response(401, "Não foi possível validar as credenciais", {"WWW-Authenticate": "Bearer"})


@app.exception_handler(ForbiddenCargoError)
def _forbidden_cargo_handler(request: Request, exc: ForbiddenCargoError):
    return _error_response(403, str(exc))


@app.exception_handler(UserNotFoundError)
def _user_not_found_handler(request: Request, exc: UserNotFoundError):
    return _error_response(404, "Usuário não encontrado")


@app.exception_handler(SalaNotFoundError)
def _sala_not_found_handler(request: Request, exc: SalaNotFoundError):
    return _error_response(404, str(exc))


@app.exception_handler(DuplicateLoginError)
def _duplicate_login_handler(request: Request, exc: DuplicateLoginError):
    return _error_response(400, "Login já cadastrado")


@app.exception_handler(CannotDeleteSelfError)
def _cannot_delete_self_handler(request: Request, exc: CannotDeleteSelfError):
    return _error_response(400, "Não é possível remover o próprio usuário")


app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(salas_router.router)


@app.get("/")
def root():
    return {"status": "ok", "escola": SCHOOL_NAME}
