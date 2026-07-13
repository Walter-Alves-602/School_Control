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

from auth.database import Base, SessionLocal, engine  # noqa: E402
from auth.models import User  # noqa: E402
from auth.security import hash_password  # noqa: E402


def create_user(name: str, login: str, password: str, cargo: str) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.login == login).first():
            print(f"❌ Já existe um usuário com o login '{login}'.")
            return

        user = User(name=name, login=login, password_hash=hash_password(password), cargo=cargo)
        db.add(user)
        db.commit()
        print(f"✅ Usuário '{login}' ({cargo}) criado com sucesso.")
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
