from utils import executar_comando_ssh, executar_comando_winrm, salvar_log


def gerar_ips(inicio, fim):
    for i in range(inicio, fim + 1):
        yield f"35.0.0.{i}"


def menu_geral():
    print("Controle de computadores")
    print("1 - Sala Paris (Windows 10)")
    print("2 - Sala Zion (Linux Mint)")
    print("3 - Sala Monitoria (Windows 10)")
    print("4 - Sair")
    return input("Escolha a sala (1, 2, 3 ou 4): ")


def executar_win(IPinicio, IPfim, usuario, senha):
    while True:
        comando = input("Comando a executar (ou sair): ")
        if comando.lower() == "sair":
            break
        resultados = []
        for ip in gerar_ips(IPinicio, IPfim):
            print(f"Executando em {ip}...")
            saida, erro = executar_comando_winrm(ip, usuario, senha, comando)
            if saida:
                print(f"Saída de {ip}:\n{saida}")
            if erro:
                print(f"Erro em {ip}:\n{erro}")
        caminho_log = salvar_log(comando, resultados)
        print(f"\nLog salvo em: {caminho_log}")


def executar_linux(IPinicio, IPfim, usuario, senha):
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
        caminho_log = salvar_log(comando, resultados)
        print(f"\nLog salvo em: {caminho_log}")


def main():
    sala = menu_geral()
    usuario = input("Usuário WinRM/SSH: ")
    senha = input("Senha WinRM/SSH: ")
    match sala:
        case "1":
            executar_win(101, 135, usuario, senha)
        case "2":
            executar_linux(136, 171, usuario, senha)
        case "3":
            executar_win(172, 175, usuario, senha)
        case "4":
            print("Saindo...")
            return
        case _:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
