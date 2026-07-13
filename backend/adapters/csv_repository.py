"""
Inventário de computadores (CSV) e configuração de salas (vinda do .env via
config.py). Implementa o port ComputerRepository (domain/ports.py).
"""

import csv
import os
from typing import Dict, List

from config import COMPUTERS_CSV_PATH, DEFAULT_CONFIG, SALAS_CONFIG
from domain.entities import Computador, Sala
from domain.ports import ComputerRepository


def _config_to_sala(nome: str, config: dict) -> Sala:
    return Sala(
        nome=nome,
        os=config["os"],
        username=config["username"],
        password=config["password"],
        ssh_port=config["ssh_port"],
        package_manager=config["package_manager"],
        sudo_required=config["sudo_required"],
        commands=config["commands"],
    )


class CsvComputerRepository(ComputerRepository):
    def __init__(self, csv_file_path: str = COMPUTERS_CSV_PATH):
        self._csv_file_path = csv_file_path

    def load_all(self) -> List[Computador]:
        computers: List[Computador] = []

        if not os.path.exists(self._csv_file_path):
            print(f"Arquivo {self._csv_file_path} não encontrado!")
            return computers

        with open(self._csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line_num, row in enumerate(reader, 2):
                mac = row.get("MAC", "").strip()
                ip = row.get("IP", "").strip().replace('"', "")
                sala = row.get("Sala", "").strip()

                if mac and ip and sala:
                    computers.append(Computador(mac=mac.replace("-", ":"), ip=ip, sala=sala))
                else:
                    print(f"Linha {line_num} incompleta: MAC='{mac}', IP='{ip}', Sala='{sala}'")

        return computers

    def get_by_sala(self, sala_name: str) -> List[Computador]:
        return [c for c in self.load_all() if c.sala.lower() == sala_name.lower()]

    def list_salas_summary(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for computer in self.load_all():
            summary[computer.sala] = summary.get(computer.sala, 0) + 1
        return summary

    def get_available_salas(self) -> List[str]:
        return list(SALAS_CONFIG.keys())

    def get_sala_config(self, sala_name: str) -> Sala:
        config = SALAS_CONFIG.get(sala_name, DEFAULT_CONFIG)
        return _config_to_sala(sala_name, config)

    def get_command_for_sala(self, sala_name: str, command_type: str, **kwargs) -> str:
        sala = self.get_sala_config(sala_name)
        template = sala.commands.get(command_type, "")
        if template and kwargs:
            return template.format(**kwargs)
        return template
