"""
API (FastAPI) do Sistema de Controle de Computadores por Salas.
Executa localmente e é consumida pela interface web (feita separadamente).

Para rodar:
    uvicorn api:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.database import Base, engine
from config import CORS_ORIGINS, SCHOOL_NAME
from routers import auth_router, salas_router, users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=f"Sistema de Controle de Computadores - {SCHOOL_NAME}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(salas_router.router)


@app.get("/")
def root():
    return {"status": "ok", "escola": SCHOOL_NAME}
