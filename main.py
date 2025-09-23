import paramiko
import socket
import time
from typing import Iterator, List, Tuple


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



# Exemplo de uso
if __name__ == "__main__":
    ips = generate_ip_range("35.0.0.", 136, 171)
    results = execute_ssh_command_on_multiple_hosts(
        command="hostname",
        ip_generator=ips,
        password="in12345678",
        use_sudo=False
    )
    print(results)