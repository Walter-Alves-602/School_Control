# -*- coding: utf-8 -*-
import winrm

def executar_comando_winrm(ip, usuario, senha, comando):
    try:
        sess = winrm.Session(f'http://{ip}:5985/wsman', auth=(usuario, senha))
        r = sess.run_cmd(comando)
        saida = r.std_out.decode()
        erro = r.std_err.decode()
        return saida, erro
    except Exception as e:
        return '', f"Erro ao conectar em {ip}: {e}"
