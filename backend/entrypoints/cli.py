"""
Sistema de Controle de Computadores por Salas - Interface de linha de comando.
Usa os mesmos casos de uso (application/) e adapters da API.
"""

import getpass
import sys
from pathlib import Path

# Permite executar este arquivo diretamente, por exemplo:
# python entrypoints/cli.py
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from adapters.csv_repository import CsvComputerRepository
from adapters.db import Base, SessionLocal, SqlAlchemyUserRepository, engine
from adapters.security import BcryptPasswordHasher
from adapters.ssh_executor import ParamikoRemoteExecutor
from adapters.wol_sender import UdpWakeOnLanSender
from application.sala_service import SalaService
from application.user_service import UserService
from config import DEFAULT_SSH_TIMEOUT, WOL_BROADCAST_IP
from domain.errors import CannotDeleteSelfError, DuplicateLoginError, UserNotFoundError

computer_repository = CsvComputerRepository()
sala_service = SalaService(
    computer_repository=computer_repository,
    remote_executor=ParamikoRemoteExecutor(),
    wol_sender=UdpWakeOnLanSender(),
    wol_broadcast_ip=WOL_BROADCAST_IP,
    default_ssh_timeout=DEFAULT_SSH_TIMEOUT,
)
password_hasher = BcryptPasswordHasher()


def show_menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 60)
    print("🏫 SISTEMA DE CONTROLE DE COMPUTADORES POR SALAS")
    print("=" * 60)
    print("📋 GERENCIAMENTO DE SALAS:")
    print("  1️⃣  Listar salas disponíveis")
    print("  2️⃣  Wake-on-LAN por sala")
    print("  3️⃣  Testar conectividade SSH")
    print("  4️⃣  Informações do sistema")
    print("\n🔧 ADMINISTRAÇÃO:")
    print("  5️⃣  Desligar computadores")
    print("  6️⃣  Reiniciar computadores")
    print("  7️⃣  Atualizar sistemas")
    print("  8️⃣  Instalar pacote")
    print("  9️⃣  Comando personalizado")
    print("  🔟 Manter acordado (temporário)")
    print("\n📊 DIAGNÓSTICO:")
    print("  11  Relatório completo de sala")
    print("\n👥 USUÁRIOS DO SISTEMA:")
    print("  12  Gerenciar usuários (TI)")
    print("\n❌ 0   Sair")
    print("-" * 60)


def show_salas_summary():
    """Mostra resumo de todas as salas."""
    print("\n📋 RESUMO DE SALAS:")
    print("-" * 50)

    salas_csv = computer_repository.list_salas_summary()
    if salas_csv:
        print("📁 Salas encontradas no CSV:")
        for sala, count in salas_csv.items():
            config = computer_repository.get_sala_config(sala)
            print(f"   🏫 {sala}: {count} computadores ({config.os})")
    else:
        print("❌ Nenhuma sala encontrada no CSV")

    salas_config = computer_repository.get_available_salas()
    print(f"\n⚙️  Salas configuradas: {len(salas_config)}")
    for sala in salas_config:
        config = computer_repository.get_sala_config(sala)
        print(f"   🔧 {sala}: {config.os} - {config.username}@port{config.ssh_port}")


def select_sala():
    """Permite selecionar uma sala."""
    salas_csv = computer_repository.list_salas_summary()

    if not salas_csv:
        print("❌ Nenhuma sala encontrada no arquivo CSV!")
        return None

    print("\n📋 Salas disponíveis:")
    sala_list = list(salas_csv.keys())

    for i, sala in enumerate(sala_list, 1):
        count = salas_csv[sala]
        config = computer_repository.get_sala_config(sala)
        print(f"  {i}. {sala} ({count} computadores - {config.os})")

    while True:
        try:
            choice = input("\nEscolha a sala (número ou nome): ").strip()

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(sala_list):
                    return sala_list[idx]

            if choice in salas_csv:
                return choice

            for sala in salas_csv:
                if choice.lower() in sala.lower():
                    return sala

            print("❌ Sala não encontrada. Tente novamente.")

        except (ValueError, KeyboardInterrupt):
            return None


def wake_on_lan_menu():
    """Menu para Wake-on-LAN."""
    sala = select_sala()
    if not sala:
        return

    print(f"\n📡 Enviando Wake-on-LAN para sala '{sala}'...")
    resultado = sala_service.wake_sala(sala)
    success_count = resultado["computadores_acordados"]

    if success_count > 0:
        print(f"✅ Wake-on-LAN enviado para {success_count} computadores!")
    else:
        print("❌ Nenhum pacote Wake-on-LAN foi enviado.")


def ssh_connectivity_menu():
    """Menu para testar conectividade SSH."""
    sala = select_sala()
    if not sala:
        return

    print(f"\n🔍 Testando conectividade SSH na sala '{sala}'...")
    resultado = sala_service.connectivity_sala(sala)
    connectivity = resultado["status"]

    if connectivity:
        connected = resultado["conectados"]
        total = resultado["total"]
        print(f"\n📊 Resultado final: {connected}/{total} computadores conectados")

        if connected < total:
            print("\n❌ Computadores sem conexão:")
            for ip, status in connectivity.items():
                if not status:
                    print(f"   • {ip}")


def system_info_menu():
    """Menu para informações do sistema."""
    sala = select_sala()
    if not sala:
        return

    print(f"\n🖥️  Coletando informações do sistema da sala '{sala}'...")
    results = sala_service.system_info_sala(sala)

    if results:
        success_count = sum(1 for _, success, _ in results if success)
        print(f"\n📊 Informações coletadas de {success_count}/{len(results)} computadores")


def poweroff_menu():
    """Menu para desligar computadores."""
    sala = select_sala()
    if not sala:
        return

    confirm = input(f"\n⚠️  Confirma o DESLIGAMENTO de todos os computadores da sala '{sala}'? (sim/não): ")
    if confirm.lower() not in ["sim", "s", "yes", "y"]:
        print("❌ Operação cancelada.")
        return

    print(f"\n🔌 Desligando computadores da sala '{sala}'...")
    results = sala_service.poweroff_sala(sala)

    if results:
        success_count = sum(1 for _, success, _ in results if success)
        print(f"✅ Comando de desligamento enviado para {success_count}/{len(results)} computadores")


def restart_menu():
    """Menu para reiniciar computadores."""
    sala = select_sala()
    if not sala:
        return

    confirm = input(f"\n⚠️  Confirma o REINÍCIO de todos os computadores da sala '{sala}'? (sim/não): ")
    if confirm.lower() not in ["sim", "s", "yes", "y"]:
        print("❌ Operação cancelada.")
        return

    print(f"\n🔄 Reiniciando computadores da sala '{sala}'...")
    results = sala_service.restart_sala(sala)

    if results:
        success_count = sum(1 for _, success, _ in results if success)
        print(f"✅ Comando de reinício enviado para {success_count}/{len(results)} computadores")


def update_systems_menu():
    """Menu para atualizar sistemas."""
    sala = select_sala()
    if not sala:
        return

    confirm = input(f"\n⚠️  Confirma a ATUALIZAÇÃO de todos os computadores da sala '{sala}'? (sim/não): ")
    if confirm.lower() not in ["sim", "s", "yes", "y"]:
        print("❌ Operação cancelada.")
        return

    print(f"\n⬆️  Atualizando sistemas da sala '{sala}'...")
    print("⏱️  Esta operação pode demorar vários minutos...")
    results = sala_service.update_sala(sala)

    if results:
        success_count = sum(1 for _, success, _ in results if success)
        print(f"✅ Atualização iniciada em {success_count}/{len(results)} computadores")


def install_package_menu():
    """Menu para instalar pacotes."""
    sala = select_sala()
    if not sala:
        return

    package = input("\n📦 Digite o nome do pacote a instalar: ").strip()
    if not package:
        print("❌ Nome do pacote não pode estar vazio.")
        return

    confirm = input(f"\n⚠️  Confirma a instalação do pacote '{package}' na sala '{sala}'? (sim/não): ")
    if confirm.lower() not in ["sim", "s", "yes", "y"]:
        print("❌ Operação cancelada.")
        return

    print(f"\n📥 Instalando pacote '{package}' na sala '{sala}'...")
    results = sala_service.install_package_sala(sala, package)

    if results:
        success_count = sum(1 for _, success, _ in results if success)
        print(f"✅ Instalação iniciada em {success_count}/{len(results)} computadores")


def custom_command_menu():
    """Menu para comando personalizado."""
    sala = select_sala()
    if not sala:
        return

    command = input("\n💻 Digite o comando a executar: ").strip()
    if not command:
        print("❌ Comando não pode estar vazio.")
        return

    use_sudo = input("🔐 Executar com sudo? (s/n): ").lower().startswith("s")

    confirm = input(f"\n⚠️  Confirma execução do comando '{command}' na sala '{sala}'? (sim/não): ")
    if confirm.lower() not in ["sim", "s", "yes", "y"]:
        print("❌ Operação cancelada.")
        return

    print(f"\n⚡ Executando comando na sala '{sala}'...")
    results = sala_service.custom_command_sala(sala, command, use_sudo)

    if results:
        success_count = sum(1 for _, success, _ in results if success)
        print(f"✅ Comando executado em {success_count}/{len(results)} computadores")


def sala_report_menu():
    """Menu para relatório completo de sala."""
    sala = select_sala()
    if not sala:
        return

    print(f"\n📊 RELATÓRIO COMPLETO - SALA '{sala}'")
    print("=" * 50)

    config = computer_repository.get_sala_config(sala)
    print(f"🖥️  Sistema Operacional: {config.os}")
    print(f"👤 Usuário: {config.username}")
    print(f"🔌 Porta SSH: {config.ssh_port}")

    sala_computers = computer_repository.get_by_sala(sala)
    print(f"💻 Total de computadores: {len(sala_computers)}")

    print("\n🔍 Testando conectividade...")
    resultado = sala_service.connectivity_sala(sala)
    connectivity = resultado["status"]

    if connectivity:
        connected = resultado["conectados"]
        print(f"✅ Conectados: {connected}/{len(connectivity)}")
        print(f"❌ Desconectados: {len(connectivity) - connected}")

        print("\n📋 Status detalhado:")
        for computer in sala_computers:
            status = "🟢 Online" if connectivity.get(computer.ip, False) else "🔴 Offline"
            print(f"   {computer.ip} ({computer.mac[-8:]}...): {status}")


def list_users_menu():
    """Lista os usuários cadastrados no sistema."""
    db = SessionLocal()
    try:
        service = UserService(SqlAlchemyUserRepository(db), password_hasher)
        users = service.list_users()
        if not users:
            print("❌ Nenhum usuário cadastrado.")
            return

        print(f"\n📋 {len(users)} usuário(s) cadastrado(s):")
        for u in users:
            status = "ativo" if u.is_active else "inativo"
            print(f"   #{u.id} {u.name} | login: {u.login} | cargo: {u.cargo} | {status}")
    finally:
        db.close()


def create_user_menu():
    """Cria um novo usuário do sistema (nome, login, senha e cargo)."""
    print("\n➕ CRIAR USUÁRIO")
    name = input("Nome completo: ").strip()
    login = input("Login: ").strip()

    if not name or not login:
        print("❌ Nome e login são obrigatórios.")
        return

    password = getpass.getpass("Senha: ")
    confirm = getpass.getpass("Confirme a senha: ")
    if not password or password != confirm:
        print("❌ As senhas não coincidem ou estão vazias.")
        return

    cargo = input("Cargo (padrão: TI): ").strip() or "TI"

    db = SessionLocal()
    try:
        service = UserService(SqlAlchemyUserRepository(db), password_hasher)
        service.create_user(name, login, password, cargo)
        print(f"✅ Usuário '{login}' ({cargo}) criado com sucesso.")
    except DuplicateLoginError:
        print(f"❌ Já existe um usuário com o login '{login}'.")
    finally:
        db.close()


def reset_password_menu():
    """Redefine a senha de um usuário existente."""
    print("\n🔑 REDEFINIR SENHA")
    login = input("Login do usuário: ").strip()

    password = getpass.getpass("Nova senha: ")
    confirm = getpass.getpass("Confirme a nova senha: ")
    if not password or password != confirm:
        print("❌ As senhas não coincidem ou estão vazias.")
        return

    db = SessionLocal()
    try:
        service = UserService(SqlAlchemyUserRepository(db), password_hasher)
        service.reset_password(login, password)
        print(f"✅ Senha de '{login}' atualizada com sucesso.")
    except UserNotFoundError:
        print(f"❌ Usuário '{login}' não encontrado.")
    finally:
        db.close()


def delete_user_menu():
    """Remove um usuário do sistema."""
    print("\n🗑️  REMOVER USUÁRIO")
    login = input("Login do usuário a remover: ").strip()

    confirm = input(f"⚠️  Confirma a remoção do usuário '{login}'? (sim/não): ")
    if confirm.lower() not in ["sim", "s", "yes", "y"]:
        print("❌ Operação cancelada.")
        return

    db = SessionLocal()
    try:
        service = UserService(SqlAlchemyUserRepository(db), password_hasher)
        service.delete_by_login(login)
        print(f"✅ Usuário '{login}' removido.")
    except UserNotFoundError:
        print(f"❌ Usuário '{login}' não encontrado.")
    except CannotDeleteSelfError:
        print("❌ Não é possível remover este usuário.")
    finally:
        db.close()


def users_menu():
    """Submenu para gerenciar usuários do sistema (correção manual via terminal)."""
    while True:
        print("\n👥 GERENCIAR USUÁRIOS")
        print("-" * 50)
        print("  1. Listar usuários")
        print("  2. Criar usuário")
        print("  3. Redefinir senha")
        print("  4. Remover usuário")
        print("  0. Voltar")

        choice = input("\nEscolha uma opção: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            list_users_menu()
        elif choice == "2":
            create_user_menu()
        elif choice == "3":
            reset_password_menu()
        elif choice == "4":
            delete_user_menu()
        else:
            print("❌ Opção inválida.")


def main():
    """Função principal do sistema."""
    print("🚀 Iniciando Sistema de Controle de Computadores por Salas...")

    Base.metadata.create_all(bind=engine)

    computers = computer_repository.load_all()
    if not computers:
        print("❌ Erro: Arquivo computadores.csv não encontrado ou vazio!")
        print("   Certifique-se de ter um arquivo CSV com formato: MAC,IP,Sala")
        return

    print(f"✅ Sistema carregado com {len(computers)} computadores")

    while True:
        try:
            show_menu()
            choice = input("Digite sua escolha: ").strip()

            if choice == "0":
                print("👋 Encerrando sistema...")
                break
            elif choice == "1":
                show_salas_summary()
            elif choice == "2":
                wake_on_lan_menu()
            elif choice == "3":
                ssh_connectivity_menu()
            elif choice == "4":
                system_info_menu()
            elif choice == "5":
                poweroff_menu()
            elif choice == "6":
                restart_menu()
            elif choice == "7":
                update_systems_menu()
            elif choice == "8":
                install_package_menu()
            elif choice == "9":
                custom_command_menu()
            elif choice == "10":
                print("🔋 Função 'Manter Acordado' não implementada nesta versão por sala")
            elif choice == "11":
                sala_report_menu()
            elif choice == "12":
                users_menu()
            else:
                print("❌ Opção inválida! Escolha um número de 0 a 12.")

        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("   Continuando execução...")


if __name__ == "__main__":
    main()
