"""
Envio de pacotes Wake-on-LAN via broadcast UDP. Implementa o port
WakeOnLanSender (domain/ports.py).
"""

import socket

from domain.ports import WakeOnLanSender


class UdpWakeOnLanSender(WakeOnLanSender):
    def send(self, mac_address: str, broadcast_ip: str) -> bool:
        try:
            mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
            magic_packet = b"\xff" * 6 + mac_bytes * 16

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, (broadcast_ip, 9))
            sock.close()

            print(f"Wake-on-LAN enviado para {mac_address}")
            return True
        except Exception as e:
            print(f"Erro ao enviar Wake-on-LAN: {e}")
            return False
