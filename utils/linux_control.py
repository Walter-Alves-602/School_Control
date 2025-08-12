
# -*- coding: utf-8 -*-
"""
Módulo para execução de comandos remotos via SSH em máquinas Linux.
"""
import paramiko
from typing import Tuple

def executar_comando_ssh(ip: str, usuario: str, senha: str, comando: str) -> Tuple[str, str]:
    """
    Executa um comando remoto via SSH.
    Args:
        ip: Endereço IP do host remoto.
        usuario: Usuário SSH.
        senha: Senha SSH.
        comando: Comando a ser executado.
    Returns:
        Uma tupla (saida, erro) com a saída padrão e erro padrão do comando.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=usuario, password=senha)
        stdin, stdout, stderr = ssh.exec_command(comando)
        saida = stdout.read().decode()
        erro = stderr.read().decode()
        ssh.close()
        return saida, erro
    except Exception as e:
        return '', f"Erro ao conectar em {ip}: {e}"
