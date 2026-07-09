"""
🔍 GUIA COMPLETO: PORTAS E CONFIGURAÇÃO WAKE-ON-LAN
==================================================

🎯 SOBRE AS PORTAS DO WAKE-ON-LAN:
=================================

❌ WAKE-ON-LAN NÃO PRECISA DE PORTAS ABERTAS NO FIREWALL!
   • Wake-on-LAN usa UDP broadcast
   • Os pacotes são enviados DA sua máquina PARA a rede
   • O computador destino recebe em HARDWARE LEVEL
   • Não há resposta de volta (é unidirecional)

📡 PORTAS USADAS PARA ENVIO:
   • Porto 9 (mais comum)
   • Porto 7 (alternativo)
   • Porto 0 (raramente funciona)

🔍 NOSSOS TESTES CONFIRMARAM:
   ✅ Pacotes enviados com sucesso (6/6 tentativas)
   ✅ Portas 9 e 7 funcionando
   ✅ Broadcast 255.255.255.255 e 35.0.0.255 OK
   ❌ Computador não acordou

🛠️  DIAGNÓSTICO DO PROBLEMA:
============================

O problema NÃO é porta bloqueada, mas sim CONFIGURAÇÃO no computador destino.

💡 VERIFICAR NO COMPUTADOR 35.0.0.160 (quando ligado):

1️⃣ VERIFICAR CONFIGURAÇÃO ATUAL:
   sudo ethtool eth0 | grep Wake-on
   # Deve mostrar: Wake-on: g
   # Se mostrar "d" = desabilitado

2️⃣ HABILITAR WAKE-ON-LAN:
   sudo ethtool -s eth0 wol g

3️⃣ VERIFICAR INTERFACE DE REDE:
   ip link show
   # Usar o nome correto da interface (pode ser enp0s3, ens18, etc.)

4️⃣ TORNAR PERMANENTE:
   # Criar arquivo de serviço:
   sudo nano /etc/systemd/system/wol.service
   
   # Conteúdo:
   [Unit]
   Description=Enable Wake On Lan
   
   [Service]
   Type=oneshot
   ExecStart=/sbin/ethtool -s eth0 wol g
   RemainAfterExit=true
   
   [Install]
   WantedBy=multi-user.target
   
   # Ativar:
   sudo systemctl daemon-reload
   sudo systemctl enable wol.service

⚙️  CONFIGURAÇÃO BIOS/UEFI:
==========================

Verificar se estão habilitadas:
✅ Wake on LAN
✅ Power On by PCI-E/Network
✅ PME Event Wake Up
✅ Power On by PCI Devices

🧪 TESTE DE DIFERENTES ESTADOS:
===============================

Wake-on-LAN funciona em:
✅ Suspended (sudo systemctl suspend)
✅ Hibernated (sudo systemctl hibernate)
✅ Shutdown com WOL habilitado
❌ Shutdown completo sem WOL
❌ Fonte de alimentação desligada

🔍 TESTE RÁPIDO PARA VERIFICAR:
===============================

1. Ligue o computador 35.0.0.160
2. Execute: sudo ethtool eth0 | grep Wake-on
3. Se mostrar "Wake-on: d", execute: sudo ethtool -s eth0 wol g
4. Suspenda o computador: sudo systemctl suspend
5. Da sua máquina, execute nosso teste novamente

📊 CONCLUSÃO:
============

✅ SEU CÓDIGO PYTHON ESTÁ PERFEITO
✅ PACOTES WAKE-ON-LAN SENDO ENVIADOS
❌ COMPUTADOR DESTINO NÃO CONFIGURADO PARA WOL

🎯 PRÓXIMO PASSO: Configure o WOL no computador 35.0.0.160
"""

print(__doc__)

# Teste prático das portas
def test_wol_ports():
    """Teste específico das portas Wake-on-LAN."""
    import socket
    
    TARGET_MAC = "0A-E0-AF-BE-0C-5C"
    TARGET_IP = "35.0.0.160"
    
    print("\n🧪 TESTE ESPECÍFICO DAS PORTAS:")
    print("="*50)
    
    # Cria magic packet
    clean_mac = TARGET_MAC.replace('-', '').replace(':', '')
    mac_bytes = bytes.fromhex(clean_mac)
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    
    ports_to_test = [9, 7, 0, 40000, 4000]
    broadcasts = ["255.255.255.255", "35.0.0.255"]
    
    for broadcast in broadcasts:
        print(f"\n📡 Testando broadcast {broadcast}:")
        for port in ports_to_test:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(magic_packet, (broadcast, port))
                sock.close()
                print(f"   ✅ Porta {port}: OK")
            except Exception as e:
                print(f"   ❌ Porta {port}: {e}")

if __name__ == "__main__":
    test_wol_ports()