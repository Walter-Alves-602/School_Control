"""
Rotas para consulta de salas e execução de comandos remotos (Wake-on-LAN,
SSH, desligar, reiniciar, atualizar, instalar pacotes, comando personalizado).
Todas as rotas exigem um usuário autenticado do cargo TI.
"""

from typing import List, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from admin_tasks import (
    execute_custom_command_sala,
    get_system_info_sala,
    install_package_sala,
    poweroff_sala,
    restart_sala,
    update_all_systems_sala,
)
from auth.deps import require_ti
from csv_manager import get_computers_by_sala, list_salas_summary, wake_computers_by_sala
from sala_config import get_available_salas, get_sala_config
from ssh_manager import test_ssh_connection_by_sala

router = APIRouter(prefix="/salas", tags=["salas"], dependencies=[Depends(require_ti)])


def _results_to_list(results: List[Tuple[str, bool, str]]) -> list:
    return [{"ip": ip, "sucesso": sucesso, "saida": saida} for ip, sucesso, saida in results]


def _require_sala_exists(sala: str) -> None:
    if not get_computers_by_sala(sala):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala '{sala}' não encontrada ou sem computadores cadastrados",
        )


@router.get("")
def list_salas():
    resumo = list_salas_summary()
    nomes = sorted(set(get_available_salas()) | set(resumo.keys()))

    return [
        {
            "sala": nome,
            "total_computadores": resumo.get(nome, 0),
            "os": get_sala_config(nome)["os"],
        }
        for nome in nomes
    ]


@router.get("/{sala}")
def get_sala(sala: str):
    computers = get_computers_by_sala(sala)
    _require_sala_exists(sala)

    config = get_sala_config(sala)
    return {
        "sala": sala,
        "os": config["os"],
        "username": config["username"],
        "ssh_port": config["ssh_port"],
        "computadores": [{"mac": mac, "ip": ip} for mac, ip, _ in computers],
    }


@router.post("/{sala}/wake")
def wake(sala: str):
    _require_sala_exists(sala)
    total = len(get_computers_by_sala(sala))
    acordados = wake_computers_by_sala(sala)
    return {"sala": sala, "total_computadores": total, "computadores_acordados": acordados}


@router.get("/{sala}/connectivity")
def connectivity(sala: str):
    _require_sala_exists(sala)
    status_por_ip = test_ssh_connection_by_sala(sala)
    conectados = sum(status_por_ip.values())
    return {"sala": sala, "conectados": conectados, "total": len(status_por_ip), "status": status_por_ip}


@router.get("/{sala}/system-info")
def system_info(sala: str):
    _require_sala_exists(sala)
    results = get_system_info_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/poweroff")
def poweroff(sala: str):
    _require_sala_exists(sala)
    results = poweroff_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/restart")
def restart(sala: str):
    _require_sala_exists(sala)
    results = restart_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/update")
def update(sala: str):
    _require_sala_exists(sala)
    results = update_all_systems_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


class InstallPackageRequest(BaseModel):
    package: str


@router.post("/{sala}/install")
def install(sala: str, payload: InstallPackageRequest):
    _require_sala_exists(sala)
    results = install_package_sala(sala, payload.package)
    return {"sala": sala, "pacote": payload.package, "resultados": _results_to_list(results)}


class CustomCommandRequest(BaseModel):
    command: str
    use_sudo: bool = False


@router.post("/{sala}/command")
def custom_command(sala: str, payload: CustomCommandRequest):
    _require_sala_exists(sala)
    results = execute_custom_command_sala(sala, payload.command, payload.use_sudo)
    return {"sala": sala, "comando": payload.command, "resultados": _results_to_list(results)}
