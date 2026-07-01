"""
Módulo para gerenciamento de suspensão/ativação e Wake-on-LAN.
"""

import socket
from typing import Iterator, List, Tuple
from ssh_manager import execute_ssh_command_on_multiple_hosts
from config import WOL_BROADCAST_IP


def prevent_sleep(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Previne que os computadores entrem em suspensão.
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command="systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=True
    )


def enable_sleep(ip_generator: Iterator[str], password: str, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Reabilita a suspensão nos computadores.
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    return execute_ssh_command_on_multiple_hosts(
        command="systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=True
    )


def wake_on_lan(mac_address: str, broadcast_ip: str = WOL_BROADCAST_IP) -> bool:
    """
    Envia pacote Wake-on-LAN para acordar computador suspenso.
    
    Args:
        mac_address (str): Endereço MAC do computador (formato: AA:BB:CC:DD:EE:FF)
        broadcast_ip (str): IP de broadcast da rede
    
    Returns:
        bool: True se o pacote foi enviado com sucesso
    """
    try:
        # Remove separadores e converte para bytes
        mac_bytes = bytes.fromhex(mac_address.replace(':', '').replace('-', ''))
        
        # Cria magic packet (6 bytes FF + 16x MAC address)
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        # Envia via UDP broadcast
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (broadcast_ip, 9))
        sock.close()
        
        print(f"Wake-on-LAN enviado para {mac_address}")
        return True
        
    except Exception as e:
        print(f"Erro ao enviar Wake-on-LAN: {e}")
        return False


def keep_awake_temporarily(ip_generator: Iterator[str], password: str, hours: int = 1, username: str = "user") -> List[Tuple[str, bool, str]]:
    """
    Mantém os computadores acordados por um período específico.
    
    Args:
        ip_generator (Iterator[str]): Gerador de IPs
        password (str): Senha do usuário
        hours (int): Número de horas para manter acordado
        username (str): Nome do usuário
    
    Returns:
        List[Tuple[str, bool, str]]: Resultados da execução
    """
    seconds = hours * 3600
    return execute_ssh_command_on_multiple_hosts(
        command=f"systemd-inhibit --what=sleep --who='SSH Session' --why='Prevent sleep for {hours}h' sleep {seconds} &",
        ip_generator=ip_generator,
        password=password,
        username=username,
        use_sudo=False
    )