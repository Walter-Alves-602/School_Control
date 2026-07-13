#!/usr/bin/env python3
"""
Teste de Portas Wake-on-LAN
Verifica se há problemas de firewall ou portas bloqueadas
"""

import socket
import subprocess
import time

TARGET_IP = "35.0.0.160"
TARGET_MAC = "0A-E0-AF-BE-0C-5C"

def check_wake_on_lan_theory():
    """Explica como funciona o Wake-on-LAN em relação a portas."""
    print("🔍 TEORIA: Como funciona Wake-on-LAN")
    print("="*50)
    print("✅ Wake-on-LAN NÃO precisa de portas abertas no destino!")
    print("✅ O magic packet é processado pela placa de rede, não pelo SO")
    print("✅ Funciona mesmo com firewall ativo")
    print("✅ Funciona mesmo com computador 'desligado'")
    print("\n📡 Portas comuns para envio:")
    print("   • Porta 9 (padrão)")
    print("   • Porta 7 (alternativa)")
    print("   • Porta 0 (algumas implementações)")
    print("\n🎯 O que importa:")
    print("   • Magic packet deve chegar à placa de rede")
    print("   • Placa de rede deve ter WOL habilitado")
    print("   • BIOS deve ter Wake-on-LAN habilitado")

def test_network_connectivity():
    """Testa conectividade de rede básica."""
    print("\n🌐 TESTE DE CONECTIVIDADE DE REDE")
    print("="*40)
    
    # Testa ping para gateway
    try:
        result = subprocess.run(['ping', '-c', '2', '35.0.0.1'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Gateway (35.0.0.1) alcançável")
        else:
            print("❌ Gateway não alcançável")
    except:
        print("❌ Erro ao testar gateway")
    
    # Testa ping para broadcast (não esperamos resposta, mas testa alcance)
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '2', '35.0.0.255'], 
                              capture_output=True, text=True, timeout=5)
        print("📡 Broadcast 35.0.0.255 testado (resposta não obrigatória)")
    except:
        print("⚠️ Problema ao alcançar broadcast")

def check_local_firewall():
    """Verifica firewall local."""
    print("\n🛡️ VERIFICAÇÃO DE FIREWALL LOCAL")
    print("="*35)
    
    # Verifica UFW
    try:
        result = subprocess.run(['sudo', 'ufw', 'status'], 
                              capture_output=True, text=True)
        print(f"🔥 UFW Status: {result.stdout.strip()}")
    except:
        print("⚠️ UFW não disponível ou erro")
    
    # Verifica iptables
    try:
        result = subprocess.run(['sudo', 'iptables', '-L', '-n'], 
                              capture_output=True, text=True)
        if "DROP" in result.stdout or "REJECT" in result.stdout:
            print("⚠️ Possíveis regras restritivas em iptables")
        else:
            print("✅ Iptables parece permissivo")
    except:
        print("⚠️ Não foi possível verificar iptables")

def test_wake_on_lan_all_ports():
    """Testa Wake-on-LAN em todas as portas possíveis."""
    print("\n📡 TESTE WAKE-ON-LAN EM MÚLTIPLAS PORTAS")
    print("="*45)
    
    # Portas comuns para WOL
    ports = [
        (9, "Porta padrão Wake-on-LAN"),
        (7, "Porta alternativa comum"),
        (40000, "Porta alta (teste de firewall)"),
        (80, "HTTP (teste de conectividade)"),
        (443, "HTTPS (teste de conectividade)")
    ]
    
    # IPs de broadcast para testar
    broadcasts = [
        ("255.255.255.255", "Broadcast global"),
        ("35.0.0.255", "Broadcast da rede"),
        (TARGET_IP, "IP específico do computador")
    ]
    
    success_count = 0
    total_tests = 0
    
    for broadcast_ip, broadcast_desc in broadcasts:
        print(f"\n🎯 Testando {broadcast_desc} ({broadcast_ip}):")
        
        for port, port_desc in ports:
            try:
                # Cria magic packet
                clean_mac = TARGET_MAC.replace('-', '').replace(':', '')
                mac_bytes = bytes.fromhex(clean_mac)
                magic_packet = b'\xff' * 6 + mac_bytes * 16
                
                # Envia pacote
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.settimeout(2)
                
                sock.sendto(magic_packet, (broadcast_ip, port))
                sock.close()
                
                print(f"   ✅ Porta {port:5d}: {port_desc}")
                success_count += 1
                
            except socket.error as e:
                print(f"   ❌ Porta {port:5d}: {e}")
            except Exception as e:
                print(f"   ❌ Porta {port:5d}: {e}")
                
            total_tests += 1
            time.sleep(0.1)
    
    print(f"\n📊 Resultado: {success_count}/{total_tests} envios bem-sucedidos")
    return success_count > 0

def test_with_different_interfaces():
    """Testa envio por diferentes interfaces de rede."""
    print("\n🔌 TESTE POR DIFERENTES INTERFACES")
    print("="*35)
    
    # Verifica interfaces disponíveis
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        print("📋 Rotas ativas:")
        for line in result.stdout.strip().split('\n')[:3]:
            print(f"   {line}")
    except:
        print("⚠️ Não foi possível verificar rotas")
    
    # Testa com diferentes interfaces usando etherwake
    interfaces = ['wlo1', 'eno1', 'eth0']
    
    for interface in interfaces:
        try:
            print(f"\n🔌 Testando interface {interface}:")
            result = subprocess.run(['sudo', 'etherwake', '-i', interface, TARGET_MAC.replace('-', ':')], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ Sucesso via {interface}")
            else:
                print(f"   ❌ Erro via {interface}: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout via {interface}")
        except Exception as e:
            print(f"   ❌ Exceção via {interface}: {e}")

def check_computer_response_extended():
    """Faz teste estendido de resposta."""
    print("\n⏰ TESTE ESTENDIDO DE RESPOSTA")
    print("="*30)
    
    print("🚀 Enviando múltiplos magic packets...")
    
    # Envia vários packets com intervalo
    for i in range(5):
        try:
            # Python socket
            clean_mac = TARGET_MAC.replace('-', '').replace(':', '')
            mac_bytes = bytes.fromhex(clean_mac)
            magic_packet = b'\xff' * 6 + mac_bytes * 16
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ("255.255.255.255", 9))
            sock.close()
            
            print(f"   📡 Packet {i+1}/5 enviado")
            time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Erro no packet {i+1}: {e}")
    
    print(f"\n⏰ Aguardando resposta por 60 segundos...")
    
    # Testa conectividade a cada 10 segundos por 1 minuto
    for i in range(6):
        time.sleep(10)
        remaining = 60 - (i+1)*10
        
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '3', TARGET_IP], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"🎉 SUCESSO! Computador respondeu após {(i+1)*10} segundos!")
                return True
            else:
                print(f"   ⏳ {remaining}s restantes...")
        except:
            print(f"   ⏳ {remaining}s restantes...")
    
    print("😴 Computador não respondeu após 60 segundos")
    return False

def show_troubleshooting_tips():
    """Mostra dicas de troubleshooting específicas para portas."""
    print("\n🛠️ TROUBLESHOOTING: PROBLEMAS DE PORTA/FIREWALL")
    print("="*55)
    
    tips = [
        "🔍 DIAGNÓSTICOS NO COMPUTADOR DESTINO (35.0.0.160):",
        "",
        "1. Verificar se WOL está realmente ativo:",
        "   sudo ethtool eth0 | grep Wake-on",
        "   # Deve mostrar 'g' para magic packet",
        "",
        "2. Verificar logs de rede:",
        "   sudo tcpdump -i eth0 port 9 or port 7",
        "   # Deve mostrar packets chegando quando enviar WOL",
        "",
        "3. Verificar firewall no destino:",
        "   sudo ufw status",
        "   sudo iptables -L -n",
        "   # WOL não precisa de portas abertas, mas logs podem ajudar",
        "",
        "4. Testar com wireshark/tcpdump:",
        "   # No computador origem:",
        "   sudo tcpdump -i wlo1 'udp and port 9'",
        "",
        "🔧 CONFIGURAÇÕES AVANÇADAS:",
        "",
        "5. Força WOL para todas as condições:",
        "   sudo ethtool -s eth0 wol pumbag",
        "   # p=physical, u=unicast, m=multicast, b=broadcast, a=arp, g=magic",
        "",
        "6. Verificar suporte na placa de rede:",
        "   sudo ethtool eth0 | grep -i wake",
        "   lspci -v | grep -A 20 Ethernet",
        "",
        "7. Configuração permanente (Ubuntu/Mint):",
        "   echo 'ethtool -s eth0 wol g' >> /etc/rc.local",
        "   # Ou criar serviço systemd",
    ]
    
    for tip in tips:
        print(tip)

def main():
    """Função principal."""
    print("🔍 DIAGNÓSTICO AVANÇADO: PORTAS E FIREWALL")
    print("🎯 Computador: 35.0.0.160 (0A-E0-AF-BE-0C-5C)")
    print("="*60)
    
    # Executa todos os testes
    check_wake_on_lan_theory()
    test_network_connectivity()
    check_local_firewall()
    
    wol_success = test_wake_on_lan_all_ports()
    
    if wol_success:
        test_with_different_interfaces()
        computer_responded = check_computer_response_extended()
        
        if computer_responded:
            print("\n🎉 PROBLEMA RESOLVIDO!")
            print("   O computador respondeu ao Wake-on-LAN!")
        else:
            print("\n🔍 PROBLEMA PERSISTE")
            print("   Packets enviados, mas computador não acordou")
            show_troubleshooting_tips()
    else:
        print("\n❌ PROBLEMA CRÍTICO: Não foi possível enviar packets")
        print("   Verifique conectividade de rede e firewall")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")