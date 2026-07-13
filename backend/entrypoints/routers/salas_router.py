"""
Rotas para consulta de salas e execução de comandos remotos (Wake-on-LAN,
SSH, desligar, reiniciar, atualizar, instalar pacotes, comando personalizado).
Todas as rotas exigem um usuário autenticado do cargo TI.
"""

from typing import List, Tuple

from fastapi import APIRouter, Depends

from application.sala_service import SalaService
from entrypoints.api_deps import get_sala_service, require_ti
from entrypoints.schemas import CustomCommandRequest, InstallPackageRequest

router = APIRouter(prefix="/salas", tags=["salas"], dependencies=[Depends(require_ti)])


def _results_to_list(results: List[Tuple[str, bool, str]]) -> list:
    return [{"ip": ip, "sucesso": sucesso, "saida": saida} for ip, sucesso, saida in results]


@router.get("")
def list_salas(sala_service: SalaService = Depends(get_sala_service)):
    return sala_service.list_salas()


@router.get("/{sala}")
def get_sala(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    return sala_service.get_sala(sala)


@router.post("/{sala}/wake")
def wake(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    return sala_service.wake_sala(sala)


@router.get("/{sala}/connectivity")
def connectivity(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    return sala_service.connectivity_sala(sala)


@router.get("/{sala}/system-info")
def system_info(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    results = sala_service.system_info_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/poweroff")
def poweroff(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    results = sala_service.poweroff_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/restart")
def restart(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    results = sala_service.restart_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/update")
def update(sala: str, sala_service: SalaService = Depends(get_sala_service)):
    results = sala_service.update_sala(sala)
    return {"sala": sala, "resultados": _results_to_list(results)}


@router.post("/{sala}/install")
def install(sala: str, payload: InstallPackageRequest, sala_service: SalaService = Depends(get_sala_service)):
    results = sala_service.install_package_sala(sala, payload.package)
    return {"sala": sala, "pacote": payload.package, "resultados": _results_to_list(results)}


@router.post("/{sala}/command")
def custom_command(
    sala: str,
    payload: CustomCommandRequest,
    sala_service: SalaService = Depends(get_sala_service),
):
    results = sala_service.custom_command_sala(sala, payload.command, payload.use_sudo)
    return {"sala": sala, "comando": payload.command, "resultados": _results_to_list(results)}
