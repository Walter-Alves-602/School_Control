# -*- coding: utf-8 -*-
import paramiko

def executar_comando_ssh(ip, usuario, senha, comando):
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
