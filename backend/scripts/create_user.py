#!/usr/bin/env python3
"""
Cria um usuário do sistema no banco SQLite (nome, login, senha e cargo).
Use para criar o primeiro usuário TI antes de acessar a API/interface web.

Exemplo:
    python scripts/create_user.py --name "Fulano da Silva" --login fulano --cargo TI
"""

import argparse
import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adapters.db import Base, SessionLocal, SqlAlchemyUserRepository, engine  # noqa: E402
from adapters.security import BcryptPasswordHasher  # noqa: E402
from application.user_service import UserService  # noqa: E402
from domain.errors import DuplicateLoginError  # noqa: E402


def create_user(name: str, login: str, password: str, cargo: str) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        service = UserService(SqlAlchemyUserRepository(db), BcryptPasswordHasher())
        try:
            service.create_user(name, login, password, cargo)
            print(f"✅ Usuário '{login}' ({cargo}) criado com sucesso.")
        except DuplicateLoginError:
            print(f"❌ Já existe um usuário com o login '{login}'.")
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Cria um usuário do sistema")
    parser.add_argument("--name", required=True, help="Nome completo do usuário")
    parser.add_argument("--login", required=True, help="Login de acesso")
    parser.add_argument("--cargo", default="TI", help="Cargo do usuário (padrão: TI)")
    args = parser.parse_args()

    password = getpass.getpass("Senha: ")
    confirm = getpass.getpass("Confirme a senha: ")
    if password != confirm:
        print("❌ As senhas não coincidem.")
        return

    create_user(args.name, args.login, password, args.cargo)


if __name__ == "__main__":
    main()
