
from utils import executar_comando_ssh, executar_comando_winrm, salvar_log
from typing import Generator

def gerar_ips(inicio: int, fim: int) -> Generator[str, None, None]:
    """
    Gera IPs no formato 35.0.0.X para o range especificado.
    """
    for i in range(inicio, fim + 1):
        yield f"35.0.0.{i}"

def menu_geral() -> str:
    """
    Exibe o menu principal e retorna a opção escolhida.
    """
    print("Controle de computadores")
    print("1 - Sala Paris (Windows 10)")
    print("2 - Sala Zion (Linux Mint)")
    print("3 - Sala Monitoria (Windows 10)")
    print("4 - Sair")
    return input("Escolha a sala (1, 2, 3 ou 4): ")

def executar_win(IPinicio: int, IPfim: int, usuario: str, senha: str, sala: str) -> None:
    """
    Executa comandos via WinRM em um range de IPs.
    """
    while True:
        comando = input("Comando a executar (ou sair): ")
        if comando.lower() == "sair":
            break
        resultados = []
        for ip in gerar_ips(IPinicio, IPfim):
            print(f"Executando em {ip}...")
            saida, erro = executar_comando_winrm(ip, usuario, senha, comando)
            resultados.append((ip, saida, erro))
            if saida:
                print(f"Saída de {ip}:\n{saida}")
            if erro:
                print(f"Erro em {ip}:\n{erro}")
        caminho_log = salvar_log(comando, resultados, sala)
        print(f"\nLog salvo em: {caminho_log}")

def executar_linux(IPinicio: int, IPfim: int, usuario: str, senha: str, sala: str) -> None:
    """
    Executa comandos via SSH em um range de IPs.
    """
    while True:
        comando = input("Comando a executar (ou sair): ")
        if comando.lower() == "sair":
            break
        resultados = []
        for ip in gerar_ips(IPinicio, IPfim):
            print(f"Executando em {ip}...")
            saida, erro = executar_comando_ssh(ip, usuario, senha, comando)
            resultados.append((ip, saida, erro))
            if saida:
                print(f"Saída de {ip}:\n{saida}")
            if erro:
                print(f"Erro em {ip}:\n{erro}")
        caminho_log = salvar_log(comando, resultados, sala)
        print(f"\nLog salvo em: {caminho_log}")

def main() -> None:
    """
    Função principal do sistema de controle de computadores.
    """
    sala = menu_geral()
    usuario = input("Usuário WinRM/SSH: ")
    senha = input("Senha WinRM/SSH: ")
    match sala:
        case "1":
            executar_win(101, 135, usuario, senha, "Paris")
        case "2":
            executar_linux(136, 171, usuario, senha, "Zion")
        case "3":
            executar_win(172, 175, usuario, senha, "Monitoria")
        case "4":
            print("Saindo...")
            return
        case _:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
