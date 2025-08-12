# -*- coding: utf-8 -*-
import os
from datetime import datetime

LOG_DIR = "logs"

def criar_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def gerar_nome_arquivo():
    agora = datetime.now()
    return agora.strftime("%Y-%m-%d-%H%M%S.txt")

def salvar_log(comando, resultados):
    criar_log_dir()
    nome_arquivo = gerar_nome_arquivo()
    caminho = os.path.join(LOG_DIR, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(f"Comando executado: {comando}\n\n")
        for ip, saida, erro in resultados:
            f.write(f"IP: {ip}\n")
            if saida:
                f.write(f"Saída:\n{saida}\n")
            if erro:
                f.write(f"Erro:\n{erro}\n")
            f.write("-"*40 + "\n")
    return caminho
