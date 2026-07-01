"""
Configurações por Sala - carregadas a partir do arquivo .env (config.py).
Cada escola define suas próprias salas e credenciais no .env; este módulo
apenas expõe funções de consulta para o restante do sistema.
"""

from config import SALAS_CONFIG, DEFAULT_CONFIG


def get_sala_config(sala_name):
    """
    Retorna a configuração específica da sala.

    Args:
        sala_name (str): Nome da sala

    Returns:
        dict: Configuração da sala
    """
    return SALAS_CONFIG.get(sala_name, DEFAULT_CONFIG)


def get_available_salas():
    """
    Retorna lista de salas disponíveis (configuradas no .env).

    Returns:
        list: Lista de nomes das salas
    """
    return list(SALAS_CONFIG.keys())


def get_command_for_sala(sala_name, command_type, **kwargs):
    """
    Retorna comando específico para a sala.

    Args:
        sala_name (str): Nome da sala
        command_type (str): Tipo do comando
        **kwargs: Parâmetros para formatação do comando

    Returns:
        str: Comando formatado
    """
    config = get_sala_config(sala_name)
    command_template = config["commands"].get(command_type, "")

    if command_template and kwargs:
        return command_template.format(**kwargs)
    return command_template
