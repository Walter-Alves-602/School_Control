"""
Casos de uso de gerenciamento de salas: consulta, Wake-on-LAN, teste de
conectividade e tarefas administrativas remotas (desligar, reiniciar,
atualizar, instalar pacote, comando personalizado).
"""

import time
from typing import List

from domain.errors import SalaNotFoundError
from domain.ports import CommandResult, ComputerRepository, RemoteExecutor, WakeOnLanSender


class SalaService:
    def __init__(
        self,
        computer_repository: ComputerRepository,
        remote_executor: RemoteExecutor,
        wol_sender: WakeOnLanSender,
        wol_broadcast_ip: str,
        default_ssh_timeout: int,
    ):
        self._computers = computer_repository
        self._executor = remote_executor
        self._wol = wol_sender
        self._broadcast_ip = wol_broadcast_ip
        self._timeout = default_ssh_timeout

    def _require_sala_exists(self, sala_name: str) -> None:
        if not self._computers.get_by_sala(sala_name):
            raise SalaNotFoundError(sala_name)

    def list_salas(self) -> List[dict]:
        resumo = self._computers.list_salas_summary()
        nomes = sorted(set(self._computers.get_available_salas()) | set(resumo.keys()))
        return [
            {
                "sala": nome,
                "total_computadores": resumo.get(nome, 0),
                "os": self._computers.get_sala_config(nome).os,
            }
            for nome in nomes
        ]

    def get_sala(self, sala_name: str) -> dict:
        computers = self._computers.get_by_sala(sala_name)
        self._require_sala_exists(sala_name)

        sala = self._computers.get_sala_config(sala_name)
        return {
            "sala": sala_name,
            "os": sala.os,
            "username": sala.username,
            "ssh_port": sala.ssh_port,
            "computadores": [{"mac": c.mac, "ip": c.ip} for c in computers],
        }

    def wake_sala(self, sala_name: str) -> dict:
        self._require_sala_exists(sala_name)
        computers = self._computers.get_by_sala(sala_name)

        acordados = 0
        for computer in computers:
            if self._wol.send(computer.mac, self._broadcast_ip):
                acordados += 1
            time.sleep(0.1)

        return {
            "sala": sala_name,
            "total_computadores": len(computers),
            "computadores_acordados": acordados,
        }

    def connectivity_sala(self, sala_name: str) -> dict:
        self._require_sala_exists(sala_name)
        sala = self._computers.get_sala_config(sala_name)
        ips = [c.ip for c in self._computers.get_by_sala(sala_name)]

        status_por_ip = self._executor.test_connectivity(
            hosts=ips,
            username=sala.username,
            password=sala.password,
            port=sala.ssh_port,
            timeout=5,
        )
        conectados = sum(status_por_ip.values())
        return {"sala": sala_name, "conectados": conectados, "total": len(status_por_ip), "status": status_por_ip}

    def system_info_sala(self, sala_name: str) -> List[CommandResult]:
        return self._run_command_sala(sala_name, "system_info", use_sudo=False)

    def poweroff_sala(self, sala_name: str) -> List[CommandResult]:
        return self._run_command_sala(sala_name, "poweroff")

    def restart_sala(self, sala_name: str) -> List[CommandResult]:
        return self._run_command_sala(sala_name, "reboot")

    def update_sala(self, sala_name: str) -> List[CommandResult]:
        return self._run_command_sala(sala_name, "update")

    def install_package_sala(self, sala_name: str, package_name: str) -> List[CommandResult]:
        return self._run_command_sala(sala_name, "install", package=package_name)

    def custom_command_sala(self, sala_name: str, command: str, use_sudo: bool = False) -> List[CommandResult]:
        self._require_sala_exists(sala_name)
        return self._run_on_sala(sala_name, command, use_sudo)

    def _run_command_sala(self, sala_name: str, command_type: str, use_sudo: bool | None = None, **kwargs) -> List[CommandResult]:
        self._require_sala_exists(sala_name)
        sala = self._computers.get_sala_config(sala_name)
        command = self._computers.get_command_for_sala(sala_name, command_type, **kwargs)
        return self._run_on_sala(sala_name, command, sala.sudo_required if use_sudo is None else use_sudo)

    def _run_on_sala(self, sala_name: str, command: str, use_sudo: bool) -> List[CommandResult]:
        sala = self._computers.get_sala_config(sala_name)
        ips = [c.ip for c in self._computers.get_by_sala(sala_name)]

        return self._executor.run(
            command=command,
            hosts=ips,
            username=sala.username,
            password=sala.password,
            port=sala.ssh_port,
            timeout=self._timeout,
            use_sudo=use_sudo,
        )
