#!/usr/bin/env python3
"""
Diagnóstico Simplificado Wake-on-LAN
Testa Wake-on-LAN para o computador 35.0.0.160
"""

import socket
import subprocess
import time
from ssh_manager import execute_ssh_command_on_multiple_hosts

# Configurações
TARGET_IP = "35.0.0.160"
TARGET_MAC = "0A-E0-AF-BE-0C-5C"
USERNAME = "aluno"
PASSWORD = "in12345678"

def test_ping():
    """Testa se o computador está respondendo."""
    print(f"🏓 Testando PING para {TARGET_IP}...")
    try:
        result = subprocess.run(['ping', '-c', '3', TARGET_IP], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Computador está respondendo ao PING")
            return True
        else:
            print("❌ Computador NÃO está respondendo ao PING")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ PING timeout - computador pode estar suspenso")
        return False
    except Exception as e:
        print(f"❌ Erro no PING: {e}")
        return False

def test_ssh():
    """Testa conectividade SSH."""
    print(f"🔐 Testando SSH para {TARGET_IP}...")
    try:
        results = execute_ssh_command_on_multiple_hosts(
            command="hostname",
            ip_generator=iter([TARGET_IP]),
            password=PASSWORD,
            username=USERNAME,
            timeout=5
        )
        
        for ip, success, output in results:
            if success:
                print(f"✅ SSH OK: {output}")
                return True
            else:
                print(f"❌ SSH falhou: {output}")
                return False
    except Exception as e:
        print(f"❌ Erro SSH: {e}")
        return False

def send_wake_on_lan_simple(mac, broadcast_ip="255.255.255.255", port=9):
    """Envia Wake-on-LAN simples."""
    try:
        # Limpa MAC e converte para bytes
        clean_mac = mac.replace('-', '').replace(':', '')
        mac_bytes = bytes.fromhex(clean_mac)
        
        # Cria magic packet
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        
        # Envia
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (broadcast_ip, port))
        sock.close()
        
        print(f"📡 WOL enviado: {mac} -> {broadcast_ip}:{port}")
        return True
        
    except Exception as e:
        print(f"❌ Erro WOL: {e}")
        return False

def test_multiple_wake_methods():
    """Testa diferentes métodos de Wake-on-LAN."""
    print("\n🚀 Testando diferentes métodos Wake-on-LAN...")
    
    # Diferentes broadcasts
    broadcasts = [
        "255.255.255.255",
        "35.0.0.255", 
        TARGET_IP
    ]
    
    # Diferentes portas
    ports = [9, 7, 0]
    
    success_count = 0
    total_attempts = 0
    
    for broadcast in broadcasts:
        for port in ports:
            print(f"🎯 Tentando {broadcast}:{port}")
            if send_wake_on_lan_simple(TARGET_MAC, broadcast, port):
                success_count += 1
            total_attempts += 1
            time.sleep(0.5)
    
    print(f"📊 Sucessos: {success_count}/{total_attempts}")
    return success_count > 0

def wait_and_check(seconds=30):
    """Aguarda e verifica se computador acordou."""
    print(f"\n⏰ Aguardando {seconds} segundos...")
    
    for i in range(seconds, 0, -5):
        print(f"   {i}s restantes...")
        time.sleep(5)
        
        # Testa ping
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '2', TARGET_IP], 
                                  capture_output=True)
            if result.returncode == 0:
                print("🎉 COMPUTADOR ACORDOU!")
                return True
        except:
            pass
    
    print("😴 Computador ainda não respondeu")
    return False

def main():
    """Função principal."""
    print("="*60)
    print("🔍 DIAGNÓSTICO WAKE-ON-LAN SIMPLIFICADO")
    print(f"🎯 Alvo: {TARGET_IP} ({TARGET_MAC})")
    print("="*60)
    
    # Teste inicial
    print("\n1️⃣ TESTE INICIAL DE CONECTIVIDADE")
    ping_ok = test_ping()
    ssh_ok = test_ssh()
    
    if ping_ok and ssh_ok:
        print("✅ Computador já está ligado e funcionando!")
        return
    
    # Teste Wake-on-LAN
    print("\n2️⃣ TESTE WAKE-ON-LAN")
    wol_sent = test_multiple_wake_methods()
    
    if wol_sent:
        print("✅ Pacotes Wake-on-LAN enviados com sucesso")
        
        # Aguarda resposta
        print("\n3️⃣ AGUARDANDO RESPOSTA")
        if wait_and_check(30):
            print("🎉 SUCESSO! Wake-on-LAN funcionou!")
        else:
            print("😞 Wake-on-LAN não funcionou")
            print("\n💡 Possíveis causas:")
            print("   • Computador está desligado (não suspenso)")
            print("   • Wake-on-LAN não está habilitado")
            print("   • Placa de rede não suporta WOL")
            print("   • Cabo de rede desconectado")
    else:
        print("❌ FALHA: Não foi possível enviar pacotes WOL")
    
    print("\n4️⃣ TESTE FINAL")
    test_ping()
    test_ssh()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")