"""
Configurações por Sala - Sistemas Operacionais e Comandos
Define configurações específicas para cada sala baseado no SO
"""

# Configurações por sala
SALAS_CONFIG = {
    "Servidor": {
        "os": "linux_mint",
        "username": "admin",
        "password": "admin123",
        "ssh_port": 22,
        "package_manager": "apt",
        "sudo_required": True,
        "commands": {
            "poweroff": "sudo poweroff",
            "reboot": "sudo reboot",
            "update": "sudo apt update && sudo apt upgrade -y",
            "install": "sudo apt install -y {package}",
            "system_info": "hostname && uname -a && df -h / && free -h",
            "keep_awake": "sudo systemd-inhibit --what=sleep --who='SSH Session' --why='Prevent sleep for {hours}h' sleep {seconds} &"
        }
    },
    
    "Paris": {
        "os": "windows_10",
        "username": "aluno",
        "password": "in12345678",
        "ssh_port": 22,
        "package_manager": "winget",
        "sudo_required": False,
        "commands": {
            "poweroff": "shutdown /s /t 0",
            "reboot": "shutdown /r /t 0",
            "update": "winget upgrade --all",
            "install": "winget install {package}",
            "system_info": "hostname && systeminfo | findstr /C:\"OS Name\" /C:\"Total Physical Memory\"",
            "keep_awake": "powercfg /change standby-timeout-ac 0"
        }
    },
    
    "Zion": {
        "os": "linux_mint",
        "username": "aluno", 
        "password": "in12345678",
        "ssh_port": 22,
        "package_manager": "apt",
        "sudo_required": True,
        "commands": {
            "poweroff": "sudo poweroff",
            "reboot": "sudo reboot", 
            "update": "sudo apt update && sudo apt upgrade -y",
            "install": "sudo apt install -y {package}",
            "system_info": "hostname && uname -a && df -h / && free -h",
            "keep_awake": "sudo systemd-inhibit --what=sleep --who='SSH Session' --why='Prevent sleep for {hours}h' sleep {seconds} &"
        }
    },
    
    "Estudio": {
        "os": "windows_10",
        "username": "aluno",
        "password": "in12345678", 
        "ssh_port": 22,
        "package_manager": "winget",
        "sudo_required": False,
        "commands": {
            "poweroff": "shutdown /s /t 0",
            "reboot": "shutdown /r /t 0",
            "update": "winget upgrade --all",
            "install": "winget install {package}",
            "system_info": "hostname && systeminfo | findstr /C:\"OS Name\" /C:\"Total Physical Memory\"",
            "keep_awake": "powercfg /change standby-timeout-ac 0"
        }
    },
    
    "Monitoria": {
        "os": "windows_10",
        "username": "aluno",
        "password": "in12345678",
        "ssh_port": 22,
        "package_manager": "winget", 
        "sudo_required": False,
        "commands": {
            "poweroff": "shutdown /s /t 0",
            "reboot": "shutdown /r /t 0",
            "update": "winget upgrade --all",
            "install": "winget install {package}",
            "system_info": "hostname && systeminfo | findstr /C:\"OS Name\" /C:\"Total Physical Memory\"",
            "keep_awake": "powercfg /change standby-timeout-ac 0"
        }
    }
}

# Configuração padrão para salas não listadas
DEFAULT_CONFIG = {
    "os": "windows_10",
    "username": "aluno",
    "password": "in12345678",
    "ssh_port": 22,
    "package_manager": "winget",
    "sudo_required": False,
    "commands": {
        "poweroff": "shutdown /s /t 0",
        "reboot": "shutdown /r /t 0",
        "update": "winget upgrade --all",
        "install": "winget install {package}",
        "system_info": "hostname && systeminfo | findstr /C:\"OS Name\" /C:\"Total Physical Memory\"",
        "keep_awake": "powercfg /change standby-timeout-ac 0"
    }
}

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
    Retorna lista de salas disponíveis.
    
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