"""
Entidades de domínio — não dependem de framework, ORM ou infraestrutura.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class User:
    id: int | None
    name: str
    login: str
    password_hash: str
    cargo: str = "TI"
    is_active: bool = True


@dataclass
class Sala:
    nome: str
    os: str
    username: str
    password: str
    ssh_port: int
    package_manager: str
    sudo_required: bool
    commands: Dict[str, str] = field(default_factory=dict)


@dataclass
class Computador:
    mac: str
    ip: str
    sala: str
