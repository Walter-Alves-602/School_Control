
# -*- coding: utf-8 -*-
"""
Módulo de logging para comandos remotos.
Gera logs com nome da sala/tipo e faz rotação automática de logs antigos.
"""
import os
from datetime import datetime, timedelta
from typing import List, Tuple

LOG_DIR = "logs"
MAX_LOG_DAYS = 30  # Quantos dias manter logs

def criar_log_dir() -> None:
    """Cria o diretório de logs se não existir."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def gerar_nome_arquivo(sala: str) -> str:
    """Gera nome de arquivo de log com sala/tipo e timestamp."""
    agora = datetime.now()
    return agora.strftime(f"%Y-%m-%d-%H%M%S_{sala}.txt")

def rotacionar_logs() -> None:
    """Remove logs antigos conforme o limite de dias definido."""
    if not os.path.exists(LOG_DIR):
        return
    limite = datetime.now() - timedelta(days=MAX_LOG_DAYS)
    for nome in os.listdir(LOG_DIR):
        caminho = os.path.join(LOG_DIR, nome)
        if os.path.isfile(caminho):
            try:
                data_str = nome.split('_')[0]
                data = datetime.strptime(data_str, "%Y-%m-%d-%H%M%S")
                if data < limite:
                    os.remove(caminho)
            except Exception:
                continue

def salvar_log(comando: str, resultados: List[Tuple[str, str, str]], sala: str) -> str:
    """
    Salva o log do comando executado, incluindo nome da sala/tipo.
    Também executa rotação de logs antigos.
    """
    criar_log_dir()
    rotacionar_logs()
    nome_arquivo = gerar_nome_arquivo(sala)
    caminho = os.path.join(LOG_DIR, nome_arquivo)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(f"Sala: {sala}\nComando executado: {comando}\n\n")
        for ip, saida, erro in resultados:
            f.write(f"IP: {ip}\n")
            if saida:
                f.write(f"Saída:\n{saida}\n")
            if erro:
                f.write(f"Erro:\n{erro}\n")
            f.write("-"*40 + "\n")
    return caminho
