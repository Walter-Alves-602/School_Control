from .linux_control import executar_comando_ssh
from .windows_control import executar_comando_winrm
from .logger import salvar_log

__all__ = [
    "executar_comando_ssh",
    "executar_comando_winrm",
    "salvar_log"
]