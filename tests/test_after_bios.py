#!/usr/bin/env python3
"""
Teste Wake-on-LAN - Após Configuração BIOS
Agora com PCI Wake Control habilitado na BIOS!
"""

import socket
import subprocess
import time

# Configurações
TARGET_IP = "35.0.0.160"
TARGET_MAC = "0A-E0-AF-BE-0C-5C"

def send_powerful_wol():
    """Envia Wake-on-LAN com método potente após configuração BIOS."""
    print(f"🚀 ENVIANDO WAKE-ON-LAN POTENTE PARA {TARGET_MAC}")
    print(f"🎯 Alvo: {TARGET_IP} (BIOS configurada com PCI Wake Control)")
    print("="*60)
    
    # Cria magic packet
    clean_mac = TARGET_MAC.replace('-', '').replace(':', '').upper()
    mac_bytes = bytes.fromhex(clean_mac)
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    
    print(f"📦 Magic Packet: {len(magic_packet)} bytes")
    print(f"🔤 Prefixo: {magic_packet[:6].hex()}")
    print(f"🔤 MAC: {mac_bytes.hex()}")
    
    success_count = 0
    
    # Configurações otimizadas após BIOS configurada
    configs = [
        ("255.255.255.255", 9, "Broadcast Geral - Porta 9"),
        ("255.255.255.255", 7, "Broadcast Geral - Porta 7"), 
        ("35.0.0.255", 9, "Broadcast Local - Porta 9"),
        ("35.0.0.255", 7, "Broadcast Local - Porta 7"),
        (TARGET_IP, 9, "Unicast Direto - Porta 9"),
        (TARGET_IP, 7, "Unicast Direto - Porta 7"),
    ]
    
    print(f"\n📡 Enviando {len(configs)} pacotes Wake-on-LAN:")
    
    for broadcast, port, description in configs:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, (broadcast, port))
            sock.close()
            
            print(f"   ✅ {description}")
            success_count += 1
            time.sleep(0.2)  # Pequena pausa entre envios
            
        except Exception as e:
            print(f"   ❌ {description}: {e}")
    
    print(f"\n📊 Pacotes enviados: {success_count}/{len(configs)}")
    return success_count > 0

def send_external_wol():
    """Envia com ferramentas externas também."""
    print(f"\n🔧 ENVIANDO COM FERRAMENTAS EXTERNAS:")
    
    try:
        print("   🚀 wakeonlan...")
        result = subprocess.run(['wakeonlan', TARGET_MAC.replace('-', ':')], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ wakeonlan: {result.stdout.strip()}")
        else:
            print(f"   ❌ wakeonlan: {result.stderr.strip()}")
    except Exception as e:
        print(f"   ❌ wakeonlan: {e}")

def intensive_monitoring(duration=60):
    """Monitora intensivamente se o computador acordou."""
    print(f"\n⏰ MONITORAMENTO INTENSIVO ({duration} segundos)")
    print("🔍 Testando conectividade a cada 2 segundos...")
    
    start_time = time.time()
    attempts = 0
    
    while time.time() - start_time < duration:
        remaining = int(duration - (time.time() - start_time))
        attempts += 1
        
        print(f"  📊 Tentativa {attempts} | ⏳ {remaining}s restantes", end=" | ")
        
        # Teste ping rápido
        try:
            result = subprocess.run(['ping', '-c', '1', '-W', '1', TARGET_IP], 
                                  capture_output=True, timeout=2)
            if result.returncode == 0:
                print("🎉 COMPUTADOR ACORDOU! 🎉")
                return True
            else:
                print("💤 Ainda dormindo...")
        except:
            print("💤 Sem resposta...")
        
        time.sleep(2)
    
    print(f"\n😴 Computador não acordou em {duration} segundos")
    return False

def test_ssh_connection():
    """Testa conexão SSH se acordou."""
    print(f"\n🔐 TESTANDO SSH...")
    
    try:
        from ssh_manager import execute_ssh_command_on_multiple_hosts
        results = execute_ssh_command_on_multiple_hosts(
            command="hostname && uptime && date",
            ip_generator=iter([TARGET_IP]),
            password="in12345678",
            username="aluno",
            timeout=10
        )
        
        for ip, success, output in results:
            if success:
                print(f"✅ SSH FUNCIONANDO!")
                print(f"📊 Resposta do computador:")
                print(f"   {output}")
                return True
            else:
                print(f"❌ SSH falhou: {output}")
                return False
                
    except Exception as e:
        print(f"❌ Erro SSH: {e}")
        return False

def main():
    """Teste principal após configuração BIOS."""
    print("🎯 TESTE WAKE-ON-LAN - BIOS CONFIGURADA!")
    print("🔧 PCI Wake Control: HABILITADO ✅")
    print("="*70)
    
    # Status inicial
    print("\n📋 1. VERIFICANDO STATUS INICIAL")
    try:
        result = subprocess.run(['ping', '-c', '2', TARGET_IP], 
                              capture_output=True, timeout=8)
        if result.returncode == 0:
            print("⚠️  Computador já está ONLINE!")
            response = input("Continuar mesmo assim? (s/n): ").lower()
            if response != 's':
                return
        else:
            print("✅ Computador está OFFLINE - perfeito para teste WOL")
    except:
        print("✅ Computador está OFFLINE - perfeito para teste WOL")
    
    # Envio Wake-on-LAN
    print("\n📋 2. ENVIANDO WAKE-ON-LAN")
    wol_sent = send_powerful_wol()
    
    if wol_sent:
        print("✅ Wake-on-LAN enviado com sucesso!")
        
        # Ferramentas externas
        send_external_wol()
        
        # Monitoramento intensivo
        print("\n📋 3. MONITORAMENTO INTENSIVO")
        woke_up = intensive_monitoring(60)
        
        if woke_up:
            print("\n📋 4. TESTE SSH")
            ssh_ok = test_ssh_connection()
            
            if ssh_ok:
                print("\n🎉🎉🎉 SUCESSO TOTAL! 🎉🎉🎉")
                print("✅ Wake-on-LAN funcionou perfeitamente!")
                print("✅ PCI Wake Control resolveu o problema!")
            else:
                print("\n✅ Computador acordou mas SSH precisa de ajustes")
        else:
            print("\n🤔 Ainda não funcionou...")
            print("💡 Possíveis próximos passos:")
            print("   • Verificar outras opções na BIOS")
            print("   • Configurar Wake-on-LAN no Linux do computador destino")
            print("   • Verificar se cabo de rede está bem conectado")
    else:
        print("❌ Não foi possível enviar Wake-on-LAN")
    
    # Status final
    print(f"\n📋 5. STATUS FINAL")
    try:
        result = subprocess.run(['ping', '-c', '2', TARGET_IP], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ Computador está ONLINE agora!")
        else:
            print("❌ Computador ainda está OFFLINE")
    except:
        print("❌ Computador ainda está OFFLINE")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Teste cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()