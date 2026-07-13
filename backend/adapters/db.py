"""
Persistência dos usuários do sistema (SQLite via SQLAlchemy).
Implementa o port UserRepository (domain/ports.py).
"""

from typing import Optional

from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import DATABASE_URL
from domain.entities import User
from domain.ports import UserRepository

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    cargo = Column(String, nullable=False, default="TI")
    is_active = Column(Boolean, nullable=False, default=True)


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        name=model.name,
        login=model.login,
        password_hash=model.password_hash,
        cargo=model.cargo,
        is_active=model.is_active,
    )


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self._db = db

    def list_all(self) -> list[User]:
        models = self._db.query(UserModel).order_by(UserModel.id).all()
        return [_to_entity(m) for m in models]

    def get_by_login(self, login: str) -> Optional[User]:
        model = self._db.query(UserModel).filter(UserModel.login == login).first()
        return _to_entity(model) if model else None

    def get_by_id(self, user_id: int) -> Optional[User]:
        model = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        return _to_entity(model) if model else None

    def add(self, user: User) -> User:
        model = UserModel(
            name=user.name,
            login=user.login,
            password_hash=user.password_hash,
            cargo=user.cargo,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def update_password(self, user: User, password_hash: str) -> None:
        model = self._db.query(UserModel).filter(UserModel.id == user.id).first()
        model.password_hash = password_hash
        self._db.commit()

    def delete(self, user: User) -> None:
        model = self._db.query(UserModel).filter(UserModel.id == user.id).first()
        self._db.delete(model)
        self._db.commit()
