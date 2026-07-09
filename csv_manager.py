"""
Módulo para gerenciamento de arquivos CSV com endereços MAC, IPs e Salas.
"""

import os
import time
import csv
from typing import List, Tuple, Dict
from power_manager import wake_on_lan
from sala_config import get_sala_config
from config import COMPUTERS_CSV_PATH, WOL_BROADCAST_IP


def load_computers_from_csv(csv_file_path: str = COMPUTERS_CSV_PATH) -> List[Tuple[str, str, str]]:
    """
    Carrega a lista de computadores com MAC, IP e Sala do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "computadores.csv")
    
    Returns:
        List[Tuple[str, str, str]]: Lista de tuplas (MAC, IP, Sala)
    """
    computers_list = []
    
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(csv_file_path):
            print(f"Arquivo {csv_file_path} não encontrado!")
            return computers_list
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for line_num, row in enumerate(csv_reader, 2):  # Linha 2 porque linha 1 é header
                try:
                    mac = row.get('MAC', '').strip()
                    ip = row.get('IP', '').strip().replace('"', '')  # Remove aspas se existirem
                    sala = row.get('Sala', '').strip()
                    
                    if mac and ip and sala:
                        # Normaliza formato do MAC (converte - para :)
                        mac_normalized = mac.replace('-', ':')
                        computers_list.append((mac_normalized, ip, sala))
                    else:
                        print(f"Linha {line_num} incompleta: MAC='{mac}', IP='{ip}', Sala='{sala}'")
                        
                except Exception as e:
                    print(f"Erro na linha {line_num}: {e}")
        
        print(f"Carregados {len(computers_list)} computadores do arquivo {csv_file_path}")
        return computers_list
        
    except Exception as e:
        print(f"Erro ao ler arquivo {csv_file_path}: {e}")
        return computers_list


def get_computers_by_sala(sala_name: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> List[Tuple[str, str, str]]:
    """
    Retorna computadores de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[Tuple[str, str, str]]: Lista de computadores da sala (MAC, IP, Sala)
    """
    all_computers = load_computers_from_csv(csv_file_path)
    return [(mac, ip, sala) for mac, ip, sala in all_computers if sala.lower() == sala_name.lower()]


def get_macs_by_sala(sala_name: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> List[str]:
    """
    Retorna apenas MACs de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[str]: Lista de endereços MAC da sala
    """
    computers = get_computers_by_sala(sala_name, csv_file_path)
    return [mac for mac, _, _ in computers]


def get_ips_by_sala(sala_name: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> List[str]:
    """
    Retorna apenas IPs de uma sala específica.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        List[str]: Lista de IPs da sala
    """
    computers = get_computers_by_sala(sala_name, csv_file_path)
    return [ip for _, ip, _ in computers]


def get_sala_by_ip(ip: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> str:
    """
    Encontra a sala de um IP específico.
    
    Args:
        ip (str): IP a procurar
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        str: Nome da sala ou string vazia se não encontrado
    """
    all_computers = load_computers_from_csv(csv_file_path)
    for _, comp_ip, sala in all_computers:
        if comp_ip == ip:
            return sala
    return ""


def get_computer_info(ip: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> Dict[str, str]:
    """
    Retorna informações completas de um computador pelo IP.
    
    Args:
        ip (str): IP do computador
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        Dict[str, str]: Dicionário com MAC, IP, Sala e configurações
    """
    all_computers = load_computers_from_csv(csv_file_path)
    
    for mac, comp_ip, sala in all_computers:
        if comp_ip == ip:
            sala_config = get_sala_config(sala)
            return {
                "mac": mac,
                "ip": comp_ip,
                "sala": sala,
                "os": sala_config["os"],
                "username": sala_config["username"],
                "password": sala_config["password"],
                "ssh_port": sala_config["ssh_port"]
            }
    
    return {}


def wake_computers_by_sala(sala_name: str, csv_file_path: str = COMPUTERS_CSV_PATH, debug: bool = False) -> int:
    """
    Envia Wake-on-LAN para todos os computadores de uma sala.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
        debug (bool): Se deve mostrar informações de debug
    
    Returns:
        int: Número de computadores acordados com sucesso
    """
    computers = get_computers_by_sala(sala_name, csv_file_path)
    
    if not computers:
        print(f"❌ Nenhum computador encontrado na sala '{sala_name}'")
        return 0
    
    print(f"📡 Enviando Wake-on-LAN para {len(computers)} computadores da sala {sala_name}...")
    
    success_count = 0
    for mac, ip, _ in computers:
        if debug:
            print(f"🔍 Acordando {ip} ({mac}) na sala {sala_name}")
            
        if wake_on_lan(mac):
            success_count += 1
        time.sleep(0.1)
    
    print(f"✅ Wake-on-LAN: {success_count}/{len(computers)} computadores da sala {sala_name}")
    return success_count


def list_salas_summary(csv_file_path: str = COMPUTERS_CSV_PATH) -> Dict[str, int]:
    """
    Lista resumo de computadores por sala.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        Dict[str, int]: Dicionário {sala: quantidade_computadores}
    """
    all_computers = load_computers_from_csv(csv_file_path)
    salas_count = {}
    
    for _, _, sala in all_computers:
        salas_count[sala] = salas_count.get(sala, 0) + 1
    
    return salas_count


def validate_sala_name(sala_name: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> bool:
    """
    Valida se o nome da sala existe no CSV.
    
    Args:
        sala_name (str): Nome da sala
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        bool: True se a sala existe
    """
    salas_summary = list_salas_summary(csv_file_path)
    return sala_name in salas_summary


# Funções para manter compatibilidade com versões antigas
def load_macs_from_csv(csv_file_path: str = COMPUTERS_CSV_PATH) -> List[Tuple[str, str]]:
    """
    DEPRECATED: Use load_computers_from_csv para funcionalidade completa.
    Mantido para compatibilidade.
    """
    computers = load_computers_from_csv(csv_file_path)
    return [(mac, ip) for mac, ip, _ in computers]


def get_macs_only(csv_file_path: str = COMPUTERS_CSV_PATH) -> List[str]:
    """
    DEPRECATED: Use get_macs_by_sala para funcionalidade por sala.
    Retorna todos os MACs (todas as salas).
    """
    computers = load_computers_from_csv(csv_file_path)
    return [mac for mac, _, _ in computers]


def get_ips_only(csv_file_path: str = COMPUTERS_CSV_PATH) -> List[str]:
    """
    DEPRECATED: Use get_ips_by_sala para funcionalidade por sala.
    Retorna todos os IPs (todas as salas).
    """
    computers = load_computers_from_csv(csv_file_path)
    return [ip for _, ip, _ in computers]


def find_mac_by_ip(ip: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> str:
    """
    Encontra o endereço MAC correspondente a um IP específico.
    
    Args:
        ip (str): IP a procurar
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        str: Endereço MAC correspondente ou string vazia se não encontrado
    """
    all_computers = load_computers_from_csv(csv_file_path)
    for mac, comp_ip, _ in all_computers:
        if comp_ip == ip:
            return mac
    return ""


def find_ip_by_mac(mac: str, csv_file_path: str = COMPUTERS_CSV_PATH) -> str:
    """
    Encontra o IP correspondente a um endereço MAC específico.
    
    Args:
        mac (str): MAC a procurar (aceita formato com : ou -)
        csv_file_path (str): Caminho para o arquivo CSV
    
    Returns:
        str: IP correspondente ou string vazia se não encontrado
    """
    mac_normalized = mac.replace('-', ':')
    all_computers = load_computers_from_csv(csv_file_path)
    
    for stored_mac, ip, _ in all_computers:
        if stored_mac == mac_normalized:
            return ip
    
    return ""


def wake_all_computers_from_csv(csv_file_path: str = COMPUTERS_CSV_PATH, broadcast_ip: str = WOL_BROADCAST_IP, debug: bool = False) -> int:
    """
    DEPRECATED: Use wake_computers_by_sala para funcionalidade por sala.
    Envia Wake-on-LAN para todos os computadores do arquivo CSV.
    """
    computers = load_computers_from_csv(csv_file_path)
    success_count = 0
    
    print(f"📡 Enviando Wake-on-LAN para {len(computers)} computadores (todas as salas)...")
    
    for mac, ip, sala in computers:
        if debug:
            print(f"🔍 Acordando {ip} ({mac}) da sala {sala}")
            
        if wake_on_lan(mac):
            success_count += 1
        time.sleep(0.1)
    
    print(f"✅ Wake-on-LAN: {success_count}/{len(computers)} computadores processados")
    return success_count