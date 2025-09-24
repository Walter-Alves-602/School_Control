#!/usr/bin/env python3
"""
Teste Wake-on-LAN - Computador Configurado
Agora que o computador 35.0.0.160 foi configurado para receber Wake-on-LAN
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

def check_current_status():
    """Verifica status atual do computador."""
    print("🔍 Verificando status atual do computador...")
    
    # Teste PING
    try:
        result = subprocess.run(['ping', '-c', '2', '-W', '3', TARGET_IP], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ PING OK: Computador {TARGET_IP} está respondendo")
            return "online"
        else:
            print(f"❌ PING FALHOU: Computador {TARGET_IP} não responde")
            return "offline"
    except subprocess.TimeoutExpired:
        print("⏰ PING TIMEOUT: Computador pode estar suspenso")
        return "suspended"
    except Exception as e:
        print(f"❌ Erro no PING: {e}")
        return "error"

def send_enhanced_wol():
    """Envia Wake-on-LAN com método melhorado."""
    print(f"\n📡 Enviando Wake-on-LAN para {TARGET_MAC} ({TARGET_IP})...")
    
    success_count = 0
    total_attempts = 0
    
    # Configurações de teste
    broadcasts = [
        "255.255.255.255",  # Broadcast geral
        "35.0.0.255",       # Broadcast da rede local
        TARGET_IP           # IP específico (unicast)
    ]
    
    ports = [9, 7]  # Portas mais comuns para WOL
    
    for broadcast in broadcasts:
        for port in ports:
            try:
                print(f"  🎯 Tentando {broadcast}:{port}")
                
                # Cria magic packet
                clean_mac = TARGET_MAC.replace('-', '').replace(':', '').upper()
                mac_bytes = bytes.fromhex(clean_mac)
                magic_packet = b'\xff' * 6 + mac_bytes * 16
                
                # Envia pacote
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(magic_packet, (broadcast, port))
                sock.close()
                
                print(f"     ✅ Enviado com sucesso")
                success_count += 1
                
            except Exception as e:
                print(f"     ❌ Erro: {e}")
            
            total_attempts += 1
            time.sleep(0.3)  # Pausa entre envios
    
    print(f"\n📊 WOL Enviado: {success_count}/{total_attempts} tentativas")
    return success_count > 0

def monitor_wake_up(timeout=45):
    """Monitora se o computador acordou após WOL."""
    print(f"\n⏰ Monitorando por {timeout} segundos se o computador acorda...")
    
    start_time = time.time()
    check_interval = 3  # Verifica a cada 3 segundos
    
    while time.time() - start_time < timeout:
        remaining = int(timeout - (time.time() - start_time))
        print(f"  ⏳ {remaining}s restantes... testando conectividade")
        
        # Teste rápido de ping
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '2', TARGET_IP], 
                                  capture_output=True, timeout=3)
            if result.returncode == 0:
                print(f"  🎉 SUCESSO! Computador {TARGET_IP} acordou!")
                return True
        except:
            pass
        
        time.sleep(check_interval)
    
    print(f"  😴 Computador não respondeu em {timeout} segundos")
    return False

def test_ssh_after_wake():
    """Testa SSH após tentativa de wake-up."""
    print(f"\n🔐 Testando SSH após Wake-on-LAN...")
    
    try:
        results = execute_ssh_command_on_multiple_hosts(
            command="hostname && uptime",
            ip_generator=iter([TARGET_IP]),
            password=PASSWORD,
            username=USERNAME,
            timeout=8
        )
        
        for ip, success, output in results:
            if success:
                print(f"✅ SSH CONECTADO: {ip}")
                print(f"📊 Output: {output}")
                return True
            else:
                print(f"❌ SSH FALHOU: {ip} - {output}")
                return False
                
    except Exception as e:
        print(f"❌ Erro SSH: {e}")
        return False

def test_external_tools():
    """Testa com ferramentas externas também."""
    print(f"\n🔧 Testando com ferramentas externas...")
    
    tools_tested = 0
    tools_success = 0
    
    # Teste wakeonlan
    try:
        print("  🚀 Executando: wakeonlan")
        result = subprocess.run(['wakeonlan', TARGET_MAC.replace('-', ':')], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"     ✅ wakeonlan: {result.stdout.strip()}")
            tools_success += 1
        else:
            print(f"     ❌ wakeonlan: {result.stderr.strip()}")
        tools_tested += 1
    except Exception as e:
        print(f"     ❌ wakeonlan: {e}")
    
    # Teste etherwake
    try:
        print("  🚀 Executando: etherwake")
        result = subprocess.run(['sudo', 'etherwake', '-i', 'wlo1', TARGET_MAC.replace('-', ':')], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"     ✅ etherwake: Enviado")
            tools_success += 1
        else:
            print(f"     ❌ etherwake: {result.stderr.strip()}")
        tools_tested += 1
    except Exception as e:
        print(f"     ❌ etherwake: {e}")
    
    print(f"  📊 Ferramentas: {tools_success}/{tools_tested} funcionaram")
    return tools_success > 0

def main():
    """Teste principal."""
    print("="*70)
    print("🧪 TESTE WAKE-ON-LAN - COMPUTADOR CONFIGURADO")
    print(f"🎯 Alvo: {TARGET_IP} ({TARGET_MAC})")
    print("="*70)
    
    # 1. Verifica status atual
    print("\n📋 ETAPA 1: Status Atual")
    initial_status = check_current_status()
    
    if initial_status == "online":
        print("⚠️  Computador está ONLINE. Para testar WOL, ele deve estar:")
        print("   • Suspenso (suspend)")
        print("   • Hibernando (hibernate)")  
        print("   • Desligado (mas com fonte ligada)")
        
        response = input("\n❓ Quer continuar mesmo assim? (s/n): ").lower()
        if response != 's':
            print("🛑 Teste cancelado. Suspenda/desligue o computador primeiro.")
            return
    
    # 2. Envia Wake-on-LAN
    print("\n📋 ETAPA 2: Enviando Wake-on-LAN")
    wol_sent = send_enhanced_wol()
    
    if not wol_sent:
        print("❌ CRÍTICO: Não foi possível enviar WOL")
        return
    
    # 3. Testa com ferramentas externas também
    print("\n📋 ETAPA 3: Ferramentas Externas")
    test_external_tools()
    
    # 4. Monitora despertar
    print("\n📋 ETAPA 4: Monitorando Despertar")
    woke_up = monitor_wake_up(45)
    
    # 5. Testa SSH se acordou
    if woke_up:
        print("\n📋 ETAPA 5: Teste SSH Final")
        ssh_ok = test_ssh_after_wake()
        
        if ssh_ok:
            print("\n🎉 SUCESSO COMPLETO! Wake-on-LAN funcionou perfeitamente!")
        else:
            print("\n⚠️  Computador acordou mas SSH falhou")
    else:
        print("\n😞 Wake-on-LAN não funcionou ainda")
        print("\n💡 Possíveis problemas:")
        print("   • Computador totalmente desligado (fonte desconectada)")
        print("   • WOL habilitado apenas para suspend, não para shutdown")
        print("   • Configuração da BIOS incompleta")
        print("   • Magic packet não chegou ao computador")
    
    # Status final
    print(f"\n📋 ETAPA 6: Status Final")
    final_status = check_current_status()
    
    if initial_status != final_status:
        print(f"✅ Status mudou: {initial_status} → {final_status}")
    else:
        print(f"❌ Status permanece: {final_status}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n⚠️ Teste interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()