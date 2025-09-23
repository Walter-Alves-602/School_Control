"""
Sistema de Controle de Computadores - Arquivo Principal
Gerencia múltiplos computadores Linux Mint via SSH e Wake-on-LAN
"""

from ssh_manager import execute_ssh_command_on_multiple_hosts, generate_ip_range
from power_manager import (keep_awake_temporarily)
from csv_manager import (
    load_macs_from_csv,
    get_ips_only,
    wake_all_computers_from_csv,
    find_mac_by_ip,
)
from admin_tasks import (
    execute_poweroff,
    install_package,
    get_system_info,
    update_all_systems,
    restart_computers,
)


def main():
    """Função principal com exemplos de uso do sistema."""

    print("=== Sistema de Controle de Computadores ===\n")

    # Configurações
    USERNAME = "aluno"
    PASSWORD = "in12345678"
    CSV_FILE = "macs.csv"

    print("📋 1. Carregando dados do CSV...")
    mac_ip_data = load_macs_from_csv(CSV_FILE)
    if mac_ip_data:
        print(f"   ✓ Carregados {len(mac_ip_data)} computadores")
        print(f"   📄 Exemplo: {mac_ip_data[0]}")
    else:
        print("   ❌ Nenhum dado encontrado no CSV")
        return

    print("\n🔍 2. Testando busca por IP específico...")
    test_ip = "35.0.0.152"
    mac_found = find_mac_by_ip(test_ip, CSV_FILE)
    if mac_found:
        print(f"   ✓ MAC para IP {test_ip}: {mac_found}")
    else:
        print(f"   ❌ MAC não encontrado para IP {test_ip}")

    print("\n📡 3. Exemplo de comandos disponíveis:")
    print("   • SSH: execute_ssh_command_on_multiple_hosts()")
    print("   • Wake-on-LAN: wake_on_lan() ou wake_all_computers_from_csv()")
    print("   • Gerenciar suspensão: prevent_sleep(), enable_sleep()")
    print("   • Admin: install_package(), execute_poweroff(), restart_computers()")

    # Exemplo de teste de conectividade (apenas 3 IPs para não sobrecarregar)
    print("\n🔌 4. Testando conectividade SSH (primeiros 3 IPs)...")
    test_ips = get_ips_only(CSV_FILE)[:3]

    if test_ips:
        results = execute_ssh_command_on_multiple_hosts(
            command="hostname",
            ip_generator=iter(test_ips),
            password=PASSWORD,
            username=USERNAME,
            use_sudo=False,
        )

        success_count = sum(1 for _, success, _ in results if success)
        print(
            f"   📊 Conectividade: {success_count}/{len(test_ips)} computadores responderam"
        )

    print("\n💡 Exemplos de uso:")
    print_usage_examples()


def print_usage_examples():
    """Imprime exemplos de como usar cada módulo."""

    examples = [
        "\n🚀 EXEMPLOS DE USO:",
        "",
        "# 1. Acordar todos os computadores:",
        "wake_all_computers_from_csv('macs.csv')",
        "",
        "# 2. Executar comando em todos (via CSV):",
        "execute_on_all_from_csv('hostname', 'senha', 'usuario')",
        "",
        "# 3. Instalar programa em todos:",
        "ips = get_ips_only('macs.csv')",
        "install_clonezilla(iter(ips), 'senha', 'usuario')",
        "",
        "# 4. Desligar todos os computadores:",
        "ips = get_ips_only('macs.csv')",
        "execute_poweroff(iter(ips), 'senha', 'usuario')",
        "",
        "# 5. Prevenir suspensão por 2 horas:",
        "ips = get_ips_only('macs.csv')",
        "keep_awake_temporarily(iter(ips), 'senha', hours=2, username='usuario')",
        "",
        "# 6. Obter informações do sistema:",
        "ips = get_ips_only('macs.csv')",
        "get_system_info(iter(ips), 'senha', 'usuario')",
        "",
        "# 7. Atualizar todos os sistemas:",
        "ips = get_ips_only('macs.csv')",
        "update_all_systems(iter(ips), 'senha', 'usuario')",
        "",
        "# 8. Gerar range de IPs:",
        "ips = generate_ip_range('192.168.1', 10, 20)",
        "execute_ssh_command_on_multiple_hosts('comando', ips, 'senha', 'usuario')",
        "",
        "# 9. Acordar computador específico:",
        "mac = find_mac_by_ip('35.0.0.152', 'macs.csv')",
        "wake_on_lan(mac)",
    ]

    for line in examples:
        print(line)


def quick_commands():
    """Funções rápidas para tarefas comuns."""

    USERNAME = "aluno"
    PASSWORD = "in12345678"
    CSV_FILE = "macs.csv"

    # Descomente as funções que desejar usar:

    # 1. Acordar todos os computadores
    # wake_all_computers_from_csv(CSV_FILE)

    # 2. Verificar conectividade de todos
    # execute_on_all_from_csv("hostname", PASSWORD, USERNAME)

    # 3. Prevenir suspensão por 1 hora
    # ips = get_ips_only(CSV_FILE)
    # keep_awake_temporarily(iter(ips), PASSWORD, hours=1, username=USERNAME)

    # 4. Obter informações básicas
    # ips = get_ips_only(CSV_FILE)
    # get_system_info(iter(ips), PASSWORD, USERNAME)

    # 5. Instalar clonezilla
    # ips = get_ips_only(CSV_FILE)
    # install_clonezilla(iter(ips), PASSWORD, USERNAME)

    print("⚠️  Funções quick_commands() estão comentadas por segurança.")
    print("    Descomente apenas as que desejar executar.")


if __name__ == "__main__":
    IPs_Zion = generate_ip_range("35.0.0", 136, 171)
    
    while True:
        operacao = input("""
Qual operação deseja realizar? 
(1) Acordar todos os computadores
(2) desligar todos os computadores
(3) Testar conectividade SSH
(4) manter acordado por 1 hora
(5) Atualizar todos os sistemas
: """)
        match operacao:
            case "1":
                qnt = wake_all_computers_from_csv("macs.csv")
                print(f"Wake-on-LAN enviado {qnt} acordados.")
            case "2":
                qnt = execute_poweroff(IPs_Zion, "in12345678", "aluno")
                print(f"Desligamento enviado {qnt} computadores.")
            case "3":
                comando = input("Qual comando deseja executar? ")
                resultado = execute_ssh_command_on_multiple_hosts(
                    comando, IPs_Zion, "in12345678", "aluno", use_sudo=True
                )
                print(resultado)
            case "4":
                resultado = keep_awake_temporarily(IPs_Zion, "in12345678", hours=1, username="aluno")
                print(resultado)
            case "5":
                resultado = update_all_systems(IPs_Zion, "in12345678", "aluno")
                print(resultado)
            case _:
                print("Operação inválida.")
