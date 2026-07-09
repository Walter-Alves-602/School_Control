"""
Modelo de usuário do sistema (armazenado no SQLite).
"""

from sqlalchemy import Boolean, Column, Integer, String

from auth.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    cargo = Column(String, nullable=False, default="TI")
    is_active = Column(Boolean, nullable=False, default=True)
