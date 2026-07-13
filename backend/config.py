"""
Configuração central do sistema, carregada a partir do arquivo .env.
Permite que o mesmo código funcione para qualquer escola, apenas
trocando o .env (IP de broadcast, lista de salas, credenciais, etc).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _env_list(name: str) -> list:
    raw = os.getenv(name, "")
    return [item.strip() for item in raw.split(",") if item.strip()]


# ---------------------------------------------------------------------------
# Escola / rede
# ---------------------------------------------------------------------------
SCHOOL_NAME = os.getenv("SCHOOL_NAME", "Escola")
WOL_BROADCAST_IP = os.getenv("WOL_BROADCAST_IP", "255.255.255.255")
COMPUTERS_CSV_PATH = os.getenv("COMPUTERS_CSV_PATH", str(BASE_DIR / "computadores.csv"))

DEFAULT_SSH_PORT = int(os.getenv("DEFAULT_SSH_PORT", "22"))
DEFAULT_SSH_TIMEOUT = int(os.getenv("DEFAULT_SSH_TIMEOUT", "10"))

SALAS = _env_list("SALAS")

DEFAULT_SALA_OS = os.getenv("DEFAULT_SALA_OS", "windows").lower()
DEFAULT_SALA_USERNAME = os.getenv("DEFAULT_SALA_USERNAME", "user")
DEFAULT_SALA_PASSWORD = os.getenv("DEFAULT_SALA_PASSWORD", "")
DEFAULT_SALA_SSH_PORT = int(os.getenv("DEFAULT_SALA_SSH_PORT", str(DEFAULT_SSH_PORT)))

# Modelos de comando genéricos por sistema operacional. Cada sala escolhe um
# desses modelos através da variável SALA_<NOME>_OS (linux ou windows).
OS_COMMAND_TEMPLATES = {
    "linux": {
        "package_manager": "apt",
        "sudo_required": True,
        "commands": {
            "poweroff": "sudo poweroff",
            "reboot": "sudo reboot",
            "update": "sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y",
            "install": "sudo apt update && sudo apt install -y {package}",
            "system_info": "hostname && uname -a && df -h / && free -h",
            "keep_awake": (
                "sudo systemd-inhibit --what=sleep --who='SSH Session' "
                "--why='Prevent sleep for {hours}h' sleep {seconds} &"
            ),
        },
    },
    "windows": {
        "package_manager": "winget",
        "sudo_required": False,
        "commands": {
            "poweroff": "shutdown /s /t 0",
            "reboot": "shutdown /r /t 0",
            "update": "winget upgrade --all",
            "install": "winget install --silent {package}",
            "system_info": (
                'hostname && systeminfo | findstr /C:"OS Name" /C:"OS Version" '
                '/C:"Total Physical Memory"'
            ),
            "keep_awake": "powercfg /change standby-timeout-ac 0",
        },
    },
}


def _build_sala_config(sala_name: str) -> dict:
    prefix = f"SALA_{sala_name.upper().replace(' ', '_')}_"
    os_name = os.getenv(prefix + "OS", DEFAULT_SALA_OS).lower()
    template = OS_COMMAND_TEMPLATES.get(os_name, OS_COMMAND_TEMPLATES[DEFAULT_SALA_OS])

    return {
        "os": os_name,
        "username": os.getenv(prefix + "USERNAME", DEFAULT_SALA_USERNAME),
        "password": os.getenv(prefix + "PASSWORD", DEFAULT_SALA_PASSWORD),
        "ssh_port": int(os.getenv(prefix + "SSH_PORT", str(DEFAULT_SALA_SSH_PORT))),
        "package_manager": template["package_manager"],
        "sudo_required": template["sudo_required"],
        "commands": dict(template["commands"]),
    }


SALAS_CONFIG = {sala: _build_sala_config(sala) for sala in SALAS}

_default_template = OS_COMMAND_TEMPLATES.get(DEFAULT_SALA_OS, OS_COMMAND_TEMPLATES["windows"])
DEFAULT_CONFIG = {
    "os": DEFAULT_SALA_OS,
    "username": DEFAULT_SALA_USERNAME,
    "password": DEFAULT_SALA_PASSWORD,
    "ssh_port": DEFAULT_SALA_SSH_PORT,
    "package_manager": _default_template["package_manager"],
    "sudo_required": _default_template["sudo_required"],
    "commands": dict(_default_template["commands"]),
}

# ---------------------------------------------------------------------------
# Autenticação / API
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'users.db'}")

# Cargo autorizado a usar o sistema (usuários com outro cargo fazem login
# normalmente, mas recebem 403 ao acessar os recursos protegidos).
ALLOWED_CARGO = os.getenv("ALLOWED_CARGO", "TI")

CORS_ORIGINS = _env_list("CORS_ORIGINS") or ["*"]
