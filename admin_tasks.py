"""
Módulo com funções especializadas para tarefas específicas de administração com suporte a salas.
"""

from typing import Iterator, List, Tuple
from ssh_manager import execute_ssh_command_on_multiple_hosts, execute_ssh_command_by_sala
from csv_manager import get_ips_only
from sala_config import get_sala_config


def execute_poweroff(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Executa comando de desligamento nos computadores (função original mantida para compatibilidade).
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command="poweroff",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=True
    )


def poweroff_sala(sala_name: str, csv_file_path: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Desliga todos os computadores de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    sala_config = get_sala_config(sala_name)
    
    if not sala_config:
        print(f"❌ Configuração não encontrada para sala '{sala_name}'")
        return []
    
    # Comando específico por sistema operacional
    if sala_config["os"] == "Windows 10":
        command = "shutdown /s /t 0"
    else:  # Linux Mint, Ubuntu Server
        command = "poweroff"
    
    return execute_ssh_command_by_sala(
        command=command,
        sala_name=sala_name,
        use_sudo=(sala_config["os"] != "Windows 10"),
        csv_file_path=csv_file_path
    )


def restart_sala(sala_name: str, csv_file_path: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Reinicia todos os computadores de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    sala_config = get_sala_config(sala_name)
    
    if not sala_config:
        print(f"❌ Configuração não encontrada para sala '{sala_name}'")
        return []
    
    # Comando específico por sistema operacional
    if sala_config["os"] == "Windows 10":
        command = "shutdown /r /t 0"
    else:  # Linux Mint, Ubuntu Server
        command = "reboot"
    
    return execute_ssh_command_by_sala(
        command=command,
        sala_name=sala_name,
        use_sudo=(sala_config["os"] != "Windows 10"),
        csv_file_path=csv_file_path
    )


def install_package_sala(sala_name: str, package_name: str, csv_file_path: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Instala um pacote em todos os computadores de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        package_name (str): Nome do pacote a instalar
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    sala_config = get_sala_config(sala_name)
    
    if not sala_config:
        print(f"❌ Configuração não encontrada para sala '{sala_name}'")
        return []
    
    # Comando específico por sistema operacional
    if sala_config["os"] == "Windows 10":
        # Para Windows, seria necessário usar chocolatey ou outro gerenciador
        command = f"choco install {package_name} -y"
    elif sala_config["os"] == "Ubuntu Server":
        command = f"apt update && apt install -y {package_name}"
    else:  # Linux Mint
        command = f"apt update && apt install -y {package_name}"
    
    return execute_ssh_command_by_sala(
        command=command,
        sala_name=sala_name,
        use_sudo=True,
        csv_file_path=csv_file_path
    )


def get_system_info_sala(sala_name: str, csv_file_path: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Coleta informações básicas do sistema dos computadores de uma sala.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    sala_config = get_sala_config(sala_name)
    
    if not sala_config:
        print(f"❌ Configuração não encontrada para sala '{sala_name}'")
        return []
    
    # Comando específico por sistema operacional
    if sala_config["os"] == "Windows 10":
        command = "hostname && systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\" && dir C:\\ && wmic computersystem get TotalPhysicalMemory"
    else:  # Linux Mint, Ubuntu Server
        command = "hostname && uname -a && df -h / && free -h"
    
    return execute_ssh_command_by_sala(
        command=command,
        sala_name=sala_name,
        use_sudo=False,
        csv_file_path=csv_file_path
    )


def update_all_systems_sala(sala_name: str, csv_file_path: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Atualiza todos os sistemas operacionais de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    sala_config = get_sala_config(sala_name)
    
    if not sala_config:
        print(f"❌ Configuração não encontrada para sala '{sala_name}'")
        return []
    
    # Comando específico por sistema operacional
    if sala_config["os"] == "Windows 10":
        command = "sfc /scannow && dism /online /cleanup-image /restorehealth"
    elif sala_config["os"] == "Ubuntu Server":
        command = "apt update && apt upgrade -y && apt autoremove -y"
    else:  # Linux Mint
        command = "apt update && apt upgrade -y && apt autoremove -y"
    
    return execute_ssh_command_by_sala(
        command=command,
        sala_name=sala_name,
        use_sudo=True,
        csv_file_path=csv_file_path
    )


def execute_custom_command_sala(sala_name: str, command: str, use_sudo: bool = False, csv_file_path: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Executa comando personalizado em uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        command (str): Comando personalizado a executar
        use_sudo (bool): Se deve usar sudo
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_by_sala(
        command=command,
        sala_name=sala_name,
        use_sudo=use_sudo,
        csv_file_path=csv_file_path
    )


# Funções originais mantidas para compatibilidade
def install_package(ip_generator: Iterator[str], password: str, package_name: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Instala um pacote via apt em múltiplos computadores (função original).
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        package_name (str): Nome do pacote a instalar
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command=f"apt update && apt install -y {package_name}",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=True
    )


def get_system_info(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Coleta informações básicas do sistema dos computadores (função original).
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command="hostname && uname -a && df -h / && free -h",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=False
    )


def update_all_systems(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Atualiza todos os sistemas operacionais (função original).
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command="apt update && apt upgrade -y",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=True
    )


def restart_computers(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Reinicia os computadores (função original).
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command="reboot",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=True
    )


def execute_on_all_from_csv(command: str, password: str, username: str = "user", use_sudo: bool = False, csv_file: str = "computadores.csv") -> List[Tuple[str, bool, str]]:
    """
    Executa um comando em todos os computadores listados no CSV (função original atualizada).
    
    Args:
        command (str): Comando a ser executado
        password (str): Senha do usuário
        username (str): Nome do usuário
        use_sudo (bool): Se deve usar sudo
        csv_file (str): Arquivo CSV com os IPs
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    ips = get_ips_only(csv_file)
    return execute_ssh_command_on_multiple_hosts(
        command=command,
        ip_generator=iter(ips),
        password=password,
        username=username,
        use_sudo=use_sudo
    )