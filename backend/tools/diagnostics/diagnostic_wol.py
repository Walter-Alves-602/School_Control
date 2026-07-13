#!/usr/bin/env python3
"""
Arquivo de Diagnóstico Wake-on-LAN
Testa e diagnostica problemas com Wake-on-LAN para um computador específico.
"""

import socket
import struct
import time
import subprocess
import sys
import os
from csv_manager import find_mac_by_ip
from power_manager import wake_on_lan, wake_on_lan_advanced
from ssh_manager import execute_ssh_command_on_multiple_hosts

# Configurações de teste
TARGET_IP = "35.0.0.160"
TARGET_MAC = "0A-E0-AF-BE-0C-5C"  # MAC do IP 35.0.0.160
USERNAME = "aluno"
PASSWORD = "in12345678"

def print_header(title):
    """Imprime um cabeçalho formatado."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_basic_connectivity():
    """Testa conectividade básica com o computador."""
    print_header("TESTE 1: Conectividade Básica")
    
    print(f"🌐 Testando conectividade com {TARGET_IP}...")
    
    # Ping test
    try:
        result = subprocess.run(['ping', '-c', '3', TARGET_IP], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ PING: Computador está respondendo")
            print(f"📊 Resultado: {result.stdout.split()[-1]}")
            return True
        else:
            print("❌ PING: Computador não está respondendo")
            print(f"📊 Erro: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ PING: Timeout - computador pode estar suspenso")
        return False
    except Exception as e:
        print(f"❌ PING: Erro - {e}")
        return False

def test_ssh_connectivity():
    """Testa conectividade SSH."""
    print_header("TESTE 2: Conectividade SSH")
    
    print(f"🔐 Testando SSH com {TARGET_IP}...")
    
    try:
        results = execute_ssh_command_on_multiple_hosts(
            command="hostname && date && uptime",
            ip_generator=iter([TARGET_IP]),
            password=PASSWORD,
            username=USERNAME,
            timeout=5
        )
        
        for ip, success, output in results:
            if success:
                print(f"✅ SSH: Conectado com sucesso ao {ip}")
                print(f"📊 Output: {output}")
                return True
            else:
                print(f"❌ SSH: Falha na conexão com {ip}")
                print(f"📊 Erro: {output}")
                return False
                
    except Exception as e:
        print(f"❌ SSH: Erro - {e}")
        return False

def test_mac_format():
    """Testa diferentes formatos de MAC address."""
    print_header("TESTE 3: Formatos de MAC Address")
    
    mac_formats = [
        TARGET_MAC,                           # 0A-E0-AF-BE-0C-5C
        TARGET_MAC.replace('-', ':'),         # 0A:E0:AF:BE:0C:5C
        TARGET_MAC.replace('-', '').lower(),  # 0ae0afbe0c5c
        TARGET_MAC.replace('-', '').upper(),  # 0AE0AFBE0C5C
    ]
    
    print(f"🏷️  MAC Original: {TARGET_MAC}")
    
    for i, mac in enumerate(mac_formats, 1):
        print(f"📝 Formato {i}: {mac}")
        try:
            # Testa se pode converter para bytes
            clean_mac = mac.replace(':', '').replace('-', '')
            mac_bytes = bytes.fromhex(clean_mac)
            print(f"   ✅ Conversão para bytes: OK ({len(mac_bytes)} bytes)")
        except ValueError as e:
            print(f"   ❌ Conversão para bytes: ERRO - {e}")

def create_magic_packet(mac_address):
    """Cria um magic packet manualmente para debug."""
    try:
        # Limpa o MAC
        clean_mac = mac_address.replace(':', '').replace('-', '').upper()
        mac_bytes = bytes.fromhex(clean_mac)
        
        # Cria magic packet
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        print(f"🎯 Magic Packet criado:")
        print(f"   📏 Tamanho: {len(magic_packet)} bytes (deve ser 102)")
        print(f"   🔤 Prefixo FF: {magic_packet[:6].hex()}")
        print(f"   🔤 MAC repetido: {magic_packet[6:18].hex()}")
        print(f"   ✅ Packet válido: {'✅' if len(magic_packet) == 102 else '❌'}")
        
        return magic_packet
        
    except Exception as e:
        print(f"❌ Erro ao criar magic packet: {e}")
        return None

def test_wake_on_lan_basic():
    """Testa Wake-on-LAN básico."""
    print_header("TESTE 4: Wake-on-LAN Básico")
    
    print(f"📡 Testando Wake-on-LAN para {TARGET_MAC}...")
    
    # Cria magic packet para debug
    magic_packet = create_magic_packet(TARGET_MAC)
    if not magic_packet:
        return False
    
    # Testa função básica
    print(f"\n🚀 Enviando Wake-on-LAN básico...")
    success = wake_on_lan(TARGET_MAC, debug=True)
    
    if success:
        print("✅ Wake-on-LAN: Pacote enviado com sucesso")
    else:
        print("❌ Wake-on-LAN: Falha no envio")
    
    return success

def test_wake_on_lan_advanced():
    """Testa Wake-on-LAN avançado com múltiplas estratégias."""
    print_header("TESTE 5: Wake-on-LAN Avançado")
    
    print(f"🎯 Testando Wake-on-LAN avançado para {TARGET_MAC} -> {TARGET_IP}...")
    
    success = wake_on_lan_advanced(TARGET_MAC, TARGET_IP, debug=True)
    
    if success:
        print("✅ Wake-on-LAN Avançado: Pelo menos uma estratégia funcionou")
    else:
        print("❌ Wake-on-LAN Avançado: Todas as estratégias falharam")
    
    return success

def test_manual_wake_on_lan():
    """Testa Wake-on-LAN manual com diferentes configurações."""
    print_header("TESTE 6: Wake-on-LAN Manual")
    
    # Diferentes IPs de broadcast para testar
    broadcast_ips = [
        "255.255.255.255",  # Broadcast geral
        "35.0.0.255",       # Broadcast da rede
        TARGET_IP,          # IP específico
    ]
    
    # Diferentes portas
    ports = [9, 7, 0, 40000]
    
    success_count = 0
    
    for broadcast_ip in broadcast_ips:
        print(f"\n📍 Testando broadcast para {broadcast_ip}:")
        
        for port in ports:
            try:
                # Cria magic packet
                clean_mac = TARGET_MAC.replace('-', '').replace(':', '')
                mac_bytes = bytes.fromhex(clean_mac)
                magic_packet = b'\xff' * 6 + mac_bytes * 16
                
                # Envia pacote
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(magic_packet, (broadcast_ip, port))
                sock.close()
                
                print(f"   ✅ Porta {port}: Pacote enviado")
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ Porta {port}: Erro - {e}")
    
    total_attempts = len(broadcast_ips) * len(ports)
    print(f"\n📊 Resultado: {success_count}/{total_attempts} tentativas bem-sucedidas")
    
    return success_count > 0

def test_network_tools():
    """Testa ferramentas de rede disponíveis."""
    print_header("TESTE 7: Ferramentas de Rede")
    
    tools = [
        ("wakeonlan", "wakeonlan"),
        ("etherwake", "etherwake"),
        ("wol", "wol"),
    ]
    
    available_tools = []
    
    for tool_name, command in tools:
        try:
            result = subprocess.run(['which', command], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {tool_name}: Disponível em {result.stdout.strip()}")
                available_tools.append((tool_name, command))
            else:
                print(f"❌ {tool_name}: Não encontrado")
        except Exception as e:
            print(f"❌ {tool_name}: Erro - {e}")
    
    # Testa ferramentas disponíveis
    if available_tools:
        print(f"\n🔧 Testando ferramentas disponíveis:")
        
        for tool_name, command in available_tools:
            try:
                if tool_name == "wakeonlan":
                    cmd = [command, TARGET_MAC.replace('-', ':')]
                elif tool_name == "etherwake":
                    cmd = ['sudo', command, TARGET_MAC.replace('-', ':')]
                elif tool_name == "wol":
                    cmd = [command, TARGET_MAC.replace('-', ':')]
                
                print(f"   🚀 Executando: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"   ✅ {tool_name}: Sucesso")
                    if result.stdout:
                        print(f"   📊 Output: {result.stdout.strip()}")
                else:
                    print(f"   ❌ {tool_name}: Erro")
                    if result.stderr:
                        print(f"   📊 Erro: {result.stderr.strip()}")
                        
            except subprocess.TimeoutExpired:
                print(f"   ⏰ {tool_name}: Timeout")
            except Exception as e:
                print(f"   ❌ {tool_name}: Erro - {e}")
    
    return len(available_tools) > 0

def wait_and_test_response(wait_time=30):
    """Aguarda e testa se o computador acordou."""
    print_header(f"TESTE 8: Aguardando Resposta ({wait_time}s)")
    
    print(f"⏰ Aguardando {wait_time} segundos para o computador acordar...")
    
    for i in range(wait_time, 0, -5):
        print(f"   ⏳ {i} segundos restantes...")
        time.sleep(5)
        
        # Testa ping a cada 5 segundos
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '2', TARGET_IP], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   🎉 SUCESSO! Computador {TARGET_IP} acordou!")
                return True
        except:
            pass
    
    print(f"   😴 Computador {TARGET_IP} ainda não respondeu")
    return False

def check_wake_on_lan_requirements():
    """Verifica se os requisitos para Wake-on-LAN estão atendidos."""
    print_header("TESTE 9: Requisitos Wake-on-LAN")
    
    requirements = [
        "🔌 Computador deve estar conectado à energia",
        "🌐 Placa de rede deve suportar Wake-on-LAN",
        "⚙️  BIOS deve ter Wake-on-LAN habilitado",
        "🐧 Sistema operacional deve ter Wake-on-LAN configurado",
        "🔗 Cabo de rede deve estar conectado (não funciona só com WiFi)",
        "📡 Rede deve permitir broadcast packets",
    ]
    
    print("📋 Requisitos para Wake-on-LAN funcionar:")
    for req in requirements:
        print(f"   {req}")
    
    print(f"\n🔍 Para verificar se Wake-on-LAN está habilitado no computador destino,")
    print(f"   execute quando ele estiver ligado: sudo ethtool eth0 | grep Wake-on")

def main():
    """Função principal de diagnóstico."""
    print("🏥 DIAGNÓSTICO WAKE-ON-LAN")
    print(f"🎯 Computador alvo: {TARGET_IP} ({TARGET_MAC})")
    print(f"👤 Usuário: {USERNAME}")
    
    # Armazena resultados dos testes
    test_results = {}
    
    # Executa todos os testes
    test_results['connectivity'] = test_basic_connectivity()
    test_results['ssh'] = test_ssh_connectivity()
    test_mac_format()  # Apenas informativo
    test_results['basic_wol'] = test_wake_on_lan_basic()
    test_results['advanced_wol'] = test_wake_on_lan_advanced()
    test_results['manual_wol'] = test_manual_wake_on_lan()
    test_results['tools'] = test_network_tools()
    check_wake_on_lan_requirements()  # Apenas informativo
    
    # Se computador não está respondendo, tenta acordar e aguarda
    if not test_results['connectivity']:
        print(f"\n🚀 Computador não está respondendo. Enviando Wake-on-LAN e aguardando...")
        wake_on_lan_advanced(TARGET_MAC, TARGET_IP, debug=True)
        test_results['wake_response'] = wait_and_test_response()
    
    # Relatório final
    print_header("RELATÓRIO FINAL")
    
    print("📊 Resultados dos testes:")
    for test_name, result in test_results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
    
    # Análise dos resultados
    print(f"\n🔬 ANÁLISE:")
    
    if test_results.get('connectivity', False):
        print("   ✅ Computador está ligado e respondendo normalmente")
        print("   💡 Wake-on-LAN não é necessário - computador já está acordado")
    
    elif any([test_results.get('basic_wol', False), 
              test_results.get('advanced_wol', False),
              test_results.get('manual_wol', False)]):
        print("   ✅ Pacotes Wake-on-LAN foram enviados com sucesso")
        
        if test_results.get('wake_response', False):
            print("   🎉 SUCESSO! Wake-on-LAN funcionou - computador acordou!")
        else:
            print("   😴 Computador não acordou após Wake-on-LAN")
            print("   💡 Possíveis causas:")
            print("     • Wake-on-LAN não está habilitado no computador")
            print("     • Computador está desligado (não apenas suspenso)")
            print("     • Placa de rede não suporta Wake-on-LAN")
            print("     • Problemas na configuração da rede")
    else:
        print("   ❌ FALHA CRÍTICA: Não foi possível enviar pacotes Wake-on-LAN")
        print("   💡 Verifique:")
        print("     • Configuração de rede")
        print("     • Permissões do sistema")
        print("     • Firewall bloqueando broadcast")
    
    print(f"\n🏁 Diagnóstico concluído!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⚠️  Diagnóstico interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante diagnóstico: {e}")
        import traceback
        traceback.print_exc()