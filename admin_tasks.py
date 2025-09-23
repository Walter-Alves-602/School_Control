"""
Módulo com funções especializadas para tarefas específicas de administração.
"""

from typing import Iterator, List, Tuple
from ssh_manager import execute_ssh_command_on_multiple_hosts
from csv_manager import get_ips_only


def execute_poweroff(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Executa comando de desligamento nos computadores.
    
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


def install_package(ip_generator: Iterator[str], password: str, package_name: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Instala um pacote via apt em múltiplos computadores.
    
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


def install_clonezilla(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Instala o Clonezilla em múltiplos computadores.
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return install_package(ip_generator, password, "clonezilla", username)


def get_system_info(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Coleta informações básicas do sistema dos computadores.
    
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
    Atualiza todos os sistemas operacionais.
    
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
    Reinicia os computadores.
    
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


def execute_on_all_from_csv(command: str, password: str, username: str = "user", use_sudo: bool = False, csv_file: str = "macs.csv") -> List[Tuple[str, bool, str]]:
    """
    Executa um comando em todos os computadores listados no CSV.
    
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