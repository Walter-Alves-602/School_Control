"""
Módulo para gerenciamento de arquivos CSV com endereços MAC e IPs.
"""

import os
import time
from typing import List, Tuple, Dict
from power_manager import wake_on_lan


def load_macs_from_csv(csv_file_path: str = "macs.csv") -> List[Tuple[str, str]]:
    """
    Carrega a lista de endereços MAC e IPs do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        List[Tuple[str, str]]: Lista de tuplas (MAC, IP)
    """
    mac_ip_list = []
    
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(csv_file_path):
            print(f"Arquivo {csv_file_path} não encontrado!")
            return mac_ip_list
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:  # Pula linhas vazias
                    continue
                
                # Remove tabs e espaços extras
                line = line.replace('\t', '').strip()
                
                # Separa MAC e IP por vírgula
                if ',' in line:
                    mac, ip = line.split(',', 1)
                    mac = mac.strip()
                    ip = ip.strip()
                    
                    # Normaliza formato do MAC (converte - para :)
                    mac_normalized = mac.replace('-', ':')
                    
                    mac_ip_list.append((mac_normalized, ip))
                else:
                    print(f"Linha {line_num} inválida: {line}")
        
        print(f"Carregados {len(mac_ip_list)} endereços MAC do arquivo {csv_file_path}")
        return mac_ip_list
        
    except Exception as e:
        print(f"Erro ao ler arquivo {csv_file_path}: {e}")
        return mac_ip_list


def get_macs_only(csv_file_path: str = "macs.csv") -> List[str]:
    """
    Retorna apenas a lista de endereços MAC do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        List[str]: Lista de endereços MAC
    """
    mac_ip_list = load_macs_from_csv(csv_file_path)
    return [mac for mac, _ in mac_ip_list]


def get_ips_only(csv_file_path: str = "macs.csv") -> List[str]:
    """
    Retorna apenas a lista de IPs do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        List[str]: Lista de IPs
    """
    mac_ip_list = load_macs_from_csv(csv_file_path)
    return [ip for _, ip in mac_ip_list]


def get_mac_ip_dict(csv_file_path: str = "macs.csv") -> Dict[str, str]:
    """
    Retorna um dicionário com mapeamento IP -> MAC.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        Dict[str, str]: Dicionário {IP: MAC}
    """
    mac_ip_list = load_macs_from_csv(csv_file_path)
    return {ip: mac for mac, ip in mac_ip_list}


def wake_all_computers_from_csv(csv_file_path: str = "macs.csv", broadcast_ip: str = "255.255.255.255") -> int:
    """
    Envia Wake-on-LAN para todos os computadores do arquivo CSV.
    
    Args:
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
        broadcast_ip (str): IP de broadcast da rede
    
    Returns:
        int: Número de pacotes Wake-on-LAN enviados com sucesso
    """
    mac_list = get_macs_only(csv_file_path)
    success_count = 0
    
    print(f"Enviando Wake-on-LAN para {len(mac_list)} computadores...")
    
    for mac in mac_list:
        if wake_on_lan(mac, broadcast_ip):
            success_count += 1
        time.sleep(0.1)  # Pequena pausa entre envios
    
    print(f"Wake-on-LAN enviado com sucesso para {success_count}/{len(mac_list)} computadores")
    return success_count


def find_mac_by_ip(ip: str, csv_file_path: str = "macs.csv") -> str:
    """
    Encontra o endereço MAC correspondente a um IP específico.
    
    Args:
        ip (str): IP a procurar
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        str: Endereço MAC correspondente ou string vazia se não encontrado
    """
    mac_ip_dict = get_mac_ip_dict(csv_file_path)
    return mac_ip_dict.get(ip, "")


def find_ip_by_mac(mac: str, csv_file_path: str = "macs.csv") -> str:
    """
    Encontra o IP correspondente a um endereço MAC específico.
    
    Args:
        mac (str): MAC a procurar (aceita formato com : ou -)
        csv_file_path (str): Caminho para o arquivo CSV (padrão: "macs.csv")
    
    Returns:
        str: IP correspondente ou string vazia se não encontrado
    """
    mac_normalized = mac.replace('-', ':')
    mac_ip_list = load_macs_from_csv(csv_file_path)
    
    for stored_mac, ip in mac_ip_list:
        if stored_mac == mac_normalized:
            return ip
    
    return ""