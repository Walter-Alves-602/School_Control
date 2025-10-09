"""
Módulo para gerenciamento de conexões e comandos SSH com suporte a salas.
"""

import paramiko
import socket
import time
from typing import Iterator, List, Tuple, Dict


def execute_ssh_command_on_multiple_hosts(
    command: str,
    ip_generator: Iterator[str],
    password: str,
    username: str = "user",
    port: int = 22,
    timeout: int = 10,
    use_sudo: bool = False
) -> List[Tuple[str, bool, str]]:
    """
    Executa um comando SSH em múltiplos computadores (função original mantida para compatibilidade).
    
    Args:
        command (str): Comando a ser executado
        ip_generator (Iterator[str]): Gerador ou lista de IPs
        password (str): Senha para autenticação SSH
        username (str): Nome do usuário (padrão: "user")
        port (int): Porta SSH (padrão: 22)
        timeout (int): Timeout de conexão em segundos (padrão: 10)
        use_sudo (bool): Se deve executar com sudo (padrão: False)
    
    Returns:
        List[Tuple[str, bool, str]]: Lista com (IP, sucesso, output/erro)
    """
    results = []
    
    # Prepara o comando com sudo se necessário
    if use_sudo and not command.startswith('sudo'):
        final_command = f"echo '{password}' | sudo -S {command}"
    else:
        final_command = command
    
    for ip in ip_generator:
        print(f"Conectando em {ip}...")
        
        try:
            # Cria cliente SSH
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Tenta conectar
            ssh_client.connect(
                hostname=ip,
                username=username,
                password=password,
                port=port,
                timeout=timeout,
                allow_agent=False,
                look_for_keys=False
            )
            
            # Executa o comando
            stdin, stdout, stderr = ssh_client.exec_command(final_command)
            
            # Se for comando com sudo, envia a senha
            if use_sudo and not command.startswith('sudo'):
                stdin.write(f"{password}\n")
                stdin.flush()
            
            # Aguarda execução
            exit_status = stdout.channel.recv_exit_status()
            
            # Coleta output
            output = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()
            
            if exit_status == 0:
                results.append((ip, True, output))
                print(f"✓ {ip}: Comando executado com sucesso")
                if output:
                    print(f"  Output: {output}")
            else:
                results.append((ip, False, error))
                print(f"✗ {ip}: Erro na execução - {error}")
            
            # Fecha conexão
            ssh_client.close()
            
        except paramiko.AuthenticationException:
            error_msg = "Erro de autenticação - verifique usuário/senha"
            results.append((ip, False, error_msg))
            print(f"✗ {ip}: {error_msg}")
            
        except paramiko.SSHException as e:
            error_msg = f"Erro SSH: {str(e)}"
            results.append((ip, False, error_msg))
            print(f"✗ {ip}: {error_msg}")
            
        except socket.timeout:
            error_msg = "Timeout de conexão"
            results.append((ip, False, error_msg))
            print(f"✗ {ip}: {error_msg}")
            
        except socket.error as e:
            error_msg = f"Erro de rede: {str(e)}"
            results.append((ip, False, error_msg))
            print(f"✗ {ip}: {error_msg}")
            
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"
            results.append((ip, False, error_msg))
            print(f"✗ {ip}: {error_msg}")
        
        # Pequena pausa entre conexões
        time.sleep(0.5)
    
    return results


def execute_ssh_command_by_sala(
    command: str,
    sala_name: str,
    use_sudo: bool = False,
    timeout: int = 10,
    csv_file_path: str = "computadores.csv"
) -> List[Tuple[str, bool, str]]:
    """
    Executa comando SSH em todos os computadores de uma sala específica.
    
    Args:
        command (str): Comando a ser executado
        sala_name (str): Nome da sala
        use_sudo (bool): Se deve executar com sudo
        timeout (int): Timeout de conexão em segundos
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, bool, str]]: Lista com (IP, sucesso, output/erro)
    """
    # Import local para evitar circular import
    from sala_config import get_sala_config
    from csv_manager import get_computers_by_sala
    
    # Pega configuração da sala
    sala_config = get_sala_config(sala_name)
    
    if not sala_config:
        print(f"❌ Configuração não encontrada para sala '{sala_name}'")
        return []
    
    # Pega computadores da sala
    computers = get_computers_by_sala(sala_name, csv_file_path)
    
    if not computers:
        print(f"❌ Nenhum computador encontrado na sala '{sala_name}'")
        return []
    
    print(f"🔧 Executando comando em {len(computers)} computadores da sala {sala_name}")
    print(f"🖥️  Sistema: {sala_config['os']}")
    print(f"📝 Comando: {command}")
    
    # Gera lista de IPs
    ip_list = [ip for _, ip, _ in computers]
    
    # Executa comando
    return execute_ssh_command_on_multiple_hosts(
        command=command,
        ip_generator=iter(ip_list),
        username=sala_config["username"],
        password=sala_config["password"],
        port=sala_config["ssh_port"],
        timeout=timeout,
        use_sudo=use_sudo
    )


def execute_ssh_command_on_specific_ip(
    command: str,
    ip: str,
    use_sudo: bool = False,
    timeout: int = 10,
    csv_file_path: str = "computadores.csv"
) -> Tuple[str, bool, str]:
    """
    Executa comando SSH em um IP específico usando configurações da sala.
    
    Args:
        command (str): Comando a ser executado
        ip (str): IP do computador
        use_sudo (bool): Se deve executar com sudo
        timeout (int): Timeout de conexão em segundos
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        Tuple[str, bool, str]: (IP, sucesso, output/erro)
    """
    # Import local para evitar circular import
    from csv_manager import get_computer_info
    
    # Pega informações do computador
    computer_info = get_computer_info(ip, csv_file_path)
    
    if not computer_info:
        error_msg = f"IP {ip} não encontrado no arquivo CSV"
        print(f"❌ {error_msg}")
        return (ip, False, error_msg)
    
    print(f"🔧 Executando comando no computador {ip} (Sala: {computer_info['sala']})")
    print(f"🖥️  Sistema: {computer_info['os']}")
    print(f"📝 Comando: {command}")
    
    # Executa comando
    results = execute_ssh_command_on_multiple_hosts(
        command=command,
        ip_generator=iter([ip]),
        username=computer_info["username"],
        password=computer_info["password"],
        port=int(computer_info["ssh_port"]),
        timeout=timeout,
        use_sudo=use_sudo
    )
    
    return results[0] if results else (ip, False, "Nenhum resultado retornado")


def test_ssh_connection_by_sala(
    sala_name: str,
    timeout: int = 5,
    csv_file_path: str = "computadores.csv"
) -> Dict[str, bool]:
    """
    Testa conectividade SSH de todos os computadores de uma sala.
    
    Args:
        sala_name (str): Nome da sala
        timeout (int): Timeout de conexão em segundos
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        Dict[str, bool]: Dicionário {IP: conectado}
    """
    # Import local para evitar circular import
    from sala_config import get_sala_config
    from csv_manager import get_computers_by_sala
    
    # Pega configuração da sala
    sala_config = get_sala_config(sala_name)
    computers = get_computers_by_sala(sala_name, csv_file_path)
    
    if not sala_config or not computers:
        print(f"❌ Sala '{sala_name}' não encontrada ou sem computadores")
        return {}
    
    print(f"🔍 Testando conectividade SSH em {len(computers)} computadores da sala {sala_name}")
    
    connectivity = {}
    
    for mac, ip, _ in computers:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh_client.connect(
                hostname=ip,
                username=sala_config["username"],
                password=sala_config["password"],
                port=sala_config["ssh_port"],
                timeout=timeout,
                allow_agent=False,
                look_for_keys=False
            )
            
            connectivity[ip] = True
            print(f"✓ {ip}: Conectado")
            ssh_client.close()
            
        except Exception as e:
            connectivity[ip] = False
            print(f"✗ {ip}: Falha na conexão - {str(e)[:50]}...")
        
        time.sleep(0.2)
    
    connected = sum(connectivity.values())
    total = len(connectivity)
    print(f"\n📊 Resultado: {connected}/{total} computadores conectados na sala {sala_name}")
    
    return connectivity


def generate_ip_range(base_ip: str, start: int, end: int) -> Iterator[str]:
    """
    Gera uma sequência de IPs (mantida para compatibilidade).
    
    Args:
        base_ip (str): IP base (ex: "192.168.1")
        start (int): Número inicial
        end (int): Número final (inclusivo)
    
    Yields:
        str: IP completo
    """
    for i in range(start, end + 1):
        yield f"{base_ip}.{i}"