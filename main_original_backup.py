import paramiko
import socket
import time
import csv
import os
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
    Executa um comando SSH em múltiplos computadores Linux Mint.
    
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


def generate_ip_range(base_ip: str, start: int, end: int) -> Iterator[str]:
    """
    Gera uma sequência de IPs.
    
    Args:
        base_ip (str): IP base (ex: "192.168.1")
        start (int): Número inicial
        end (int): Número final (inclusivo)
    
    Yields:
        str: IP completo
    """
    for i in range(start, end + 1):
        yield f"{base_ip}.{i}"


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


def wake_on_lan(mac_address: str, broadcast_ip: str = "255.255.255.255") -> bool:
    """
    Envia pacote Wake-on-LAN para acordar computador suspenso.
    
    Args:
        mac_address (str): Endereço MAC do computador (formato: AA:BB:CC:DD:EE:FF)
        broadcast_ip (str): IP de broadcast da rede
    
    Returns:
        bool: True se o pacote foi enviado com sucesso
    """
    try:
        import socket
        
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


def load_macs_from_csv(csv_file_path: str = "macs.csv") -> List[Tuple[str, str]]:
    """
    Carrega a lista de endereços MAC e IPs do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        List[Tuple[str, str]]: Lista de tuplas (MAC, IP)
    """
    mac_ip_list = []
    
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(csv_file_path):
            print(f"Arquivo {csv_file_path} não encontrado!")
            return mac_ip_list
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:  # Pula linhas vazias
                    continue
                
                # Remove tabs e espaços extras
                line = line.replace('\t', '').strip()
                
                # Separa MAC e IP por vírgula
                if ',' in line:
                    mac, ip = line.split(',', 1)
                    mac = mac.strip()
                    ip = ip.strip()
                    
                    # Normaliza formato do MAC (converte - para :)
                    mac_normalized = mac.replace('-', ':')
                    
                    mac_ip_list.append((mac_normalized, ip))
                else:
                    print(f"Linha {line_num} inválida: {line}")
        
        print(f"Carregados {len(mac_ip_list)} endereços MAC do arquivo {csv_file_path}")
        return mac_ip_list
        
    except Exception as e:
        print(f"Erro ao ler arquivo {csv_file_path}: {e}")
        return mac_ip_list


def get_macs_only(csv_file_path: str = "macs.csv") -> List[str]:
    """
    Retorna apenas a lista de endereços MAC do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        List[str]: Lista de endereços MAC
    """
    mac_ip_list = load_macs_from_csv(csv_file_path)
    return [mac for mac, _ in mac_ip_list]


def get_ips_only(csv_file_path: str = "macs.csv") -> List[str]:
    """
    Retorna apenas a lista de IPs do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        List[str]: Lista de IPs
    """
    mac_ip_list = load_macs_from_csv(csv_file_path)
    return [ip for _, ip in mac_ip_list]


def get_mac_ip_dict(csv_file_path: str = "macs.csv") -> Dict[str, str]:
    """
    Retorna um dicionário com mapeamento IP -> MAC.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        Dict[str, str]: Dicionário {IP: MAC}
    """
    mac_ip_list = load_macs_from_csv(csv_file_path)
    return {ip: mac for mac, ip in mac_ip_list}


def wake_all_computers_from_csv(csv_file_path: str = "macs.csv", broadcast_ip: str = "255.255.255.255") -> int:
    """
    Envia Wake-on-LAN para todos os computadores do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
        broadcast_ip (str): IP de broadcast da rede
    
    Returns:
        int: Número de pacotes Wake-on-LAN enviados com sucesso
    """
    mac_list = get_macs_only(csv_file_path)
    success_count = 0
    
    print(f"Enviando Wake-on-LAN para {len(mac_list)} computadores...")
    
    for mac in mac_list:
        if wake_on_lan(mac, broadcast_ip):
            success_count += 1
        time.sleep(0.1)  # Pequena pausa entre envios
    
    print(f"Wake-on-LAN enviado com sucesso para {success_count}/{len(mac_list)} computadores")
    return success_count


def find_mac_by_ip(ip: str, csv_file_path: str = "macs.csv") -> str:
    """
    Encontra o endereço MAC correspondente a um IP específico.
    
    Args:
        ip (str): IP a procurar
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        str: Endereço MAC correspondente ou string vazia se não encontrado
    """
    mac_ip_dict = get_mac_ip_dict(csv_file_path)
    return mac_ip_dict.get(ip, "")


def find_ip_by_mac(mac: str, csv_file_path: str = "macs.csv") -> str:
    """
    Encontra o IP correspondente a um endereço MAC específico.
    
    Args:
        mac (str): MAC a procurar (aceita formato com : ou -)
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        str: IP correspondente ou string vazia se não encontrado
    """
    mac_normalized = mac.replace('-', ':')
    mac_ip_list = load_macs_from_csv(csv_file_path)
    
    for stored_mac, ip in mac_ip_list:
        if stored_mac == mac_normalized:
            return ip
    
    return ""



# Exemplo de uso
if __name__ == "__main__":
    print("=== Testando funções de MAC/IP ===\n")
    
    # 1. Carregar dados do CSV
    print("1. Carregando MACs e IPs do arquivo:")
    mac_ip_data = load_macs_from_csv("macs.csv")
    print(f"Primeiros 3 registros: {mac_ip_data[:3]}\n")
    
    # 2. Obter apenas lista de MACs
    print("2. Lista de MACs:")
    macs = get_macs_only("macs.csv")
    print(f"Total: {len(macs)} MACs")
    print(f"Primeiros 3: {macs[:3]}\n")
    
    # 3. Obter apenas lista de IPs
    print("3. Lista de IPs:")
    ips_from_csv = get_ips_only("macs.csv")
    print(f"Total: {len(ips_from_csv)} IPs")
    print(f"Primeiros 3: {ips_from_csv[:3]}\n")
    
    # 4. Buscar MAC por IP
    test_ip = "35.0.0.152"
    mac_found = find_mac_by_ip(test_ip, "macs.csv")
    print(f"4. MAC para IP {test_ip}: {mac_found}\n")
    
    # 5. Buscar IP por MAC
    test_mac = "0A:E0:AF:A2:12:53"
    ip_found = find_ip_by_mac(test_mac, "macs.csv")
    print(f"5. IP para MAC {test_mac}: {ip_found}\n")
    
    # 6. Exemplo prático: Wake-on-LAN para todos (descomente para usar)
    # print("6. Enviando Wake-on-LAN para todos os computadores:")
    # wake_all_computers_from_csv("macs.csv")
    
    # 7. Exemplo prático: SSH usando IPs do CSV
    print("7. Testando SSH nos IPs do CSV (apenas os 3 primeiros):")
    test_ips = ips_from_csv[:3]  # Testa apenas os 3 primeiros
    results = execute_ssh_command_on_multiple_hosts(
        command="hostname",
        ip_generator=iter(test_ips),
        password="in12345678",
        use_sudo=False,
        username="aluno",
    )
    print(f"Resultados: {results}\n")
    
    print("=== Exemplos de uso das novas funções ===")
    print("# Acordar todos os computadores do CSV:")
    print("# wake_all_computers_from_csv('macs.csv')")
    print()
    print("# Usar IPs do CSV para comandos SSH:")
    print("# ips = get_ips_only('macs.csv')")
    print("# execute_ssh_command_on_multiple_hosts('comando', iter(ips), 'senha', 'usuario')")
    print()
    print("# Encontrar MAC de um IP específico:")
    print("# mac = find_mac_by_ip('35.0.0.152', 'macs.csv')")
    print("# wake_on_lan(mac)")  # Acordar computador específico
