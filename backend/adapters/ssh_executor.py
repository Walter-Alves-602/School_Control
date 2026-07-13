"""
Execução de comandos remotos via SSH (paramiko). Implementa o port
RemoteExecutor (domain/ports.py).
"""

import socket
import time
from typing import Dict, List

import paramiko

from domain.ports import CommandResult, RemoteExecutor


class ParamikoRemoteExecutor(RemoteExecutor):
    def run(
        self,
        command: str,
        hosts: List[str],
        username: str,
        password: str,
        port: int,
        timeout: int,
        use_sudo: bool = False,
    ) -> List[CommandResult]:
        results: List[CommandResult] = []

        if use_sudo and not command.startswith("sudo"):
            final_command = f"echo '{password}' | sudo -S {command}"
        else:
            final_command = command

        for ip in hosts:
            print(f"Conectando em {ip}...")

            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(
                    hostname=ip,
                    username=username,
                    password=password,
                    port=port,
                    timeout=timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )

                stdin, stdout, stderr = ssh_client.exec_command(final_command)

                if use_sudo and not command.startswith("sudo"):
                    stdin.write(f"{password}\n")
                    stdin.flush()

                exit_status = stdout.channel.recv_exit_status()
                output = stdout.read().decode("utf-8").strip()
                error = stderr.read().decode("utf-8").strip()

                if exit_status == 0:
                    results.append((ip, True, output))
                    print(f"✓ {ip}: Comando executado com sucesso")
                    if output:
                        print(f"  Output: {output}")
                else:
                    results.append((ip, False, error))
                    print(f"✗ {ip}: Erro na execução - {error}")

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

            time.sleep(0.5)

        return results

    def test_connectivity(
        self,
        hosts: List[str],
        username: str,
        password: str,
        port: int,
        timeout: int,
    ) -> Dict[str, bool]:
        connectivity: Dict[str, bool] = {}

        for ip in hosts:
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(
                    hostname=ip,
                    username=username,
                    password=password,
                    port=port,
                    timeout=timeout,
                    allow_agent=False,
                    look_for_keys=False,
                )
                connectivity[ip] = True
                print(f"✓ {ip}: Conectado")
                ssh_client.close()
            except Exception as e:
                connectivity[ip] = False
                print(f"✗ {ip}: Falha na conexão - {str(e)[:50]}...")

            time.sleep(0.2)

        return connectivity
