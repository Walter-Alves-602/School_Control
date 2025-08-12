
# -*- coding: utf-8 -*-
"""
Módulo para execução de comandos remotos via WinRM em máquinas Windows.
"""
import winrm
from typing import Tuple

def executar_comando_winrm(ip: str, usuario: str, senha: str, comando: str) -> Tuple[str, str]:
    """
    Executa um comando remoto via WinRM.
    Args:
        ip: Endereço IP do host remoto.
        usuario: Usuário WinRM.
        senha: Senha WinRM.
        comando: Comando a ser executado.
    Returns:
        Uma tupla (saida, erro) com a saída padrão e erro padrão do comando.
    """
    try:
        sess = winrm.Session(f'http://{ip}:5985/wsman', auth=(usuario, senha))
        r = sess.run_cmd(comando)
        saida = r.std_out.decode()
        erro = r.std_err.decode()
        return saida, erro
    except Exception as e:
        return '', f"Erro ao conectar em {ip}: {e}"
