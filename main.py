from utils import executar_comando_ssh, executar_comando_winrm, salvar_log


def gerar_ips(inicio, fim):
    for i in range(inicio, fim + 1):
        yield f"35.0.0.{i}"


def main():
    while True:
        print("Controle de computadores")
        print("1 - Sala Paris (Windows 10)")
        print("2 - Sala Zion (Linux Mint)")
        print("3 - Sala Monitoria (Windows 10)")
        print("4 - Sair")
        sala = input("Escolha a sala (1, 2, 3 ou 4): ")
        match sala:
            case "1":
                usuario = input("Usuário WinRM: ")
                senha = input("Senha WinRM: ")
                comando = input("Comando a executar: ")
                inicio_ip = 101
                fim_ip = 135
                resultados = []
                for ip in gerar_ips(inicio_ip, fim_ip):
                    print(f"Executando em {ip}...")
                    saida, erro = executar_comando_winrm(ip, usuario, senha, comando)
                    resultados.append((ip, saida, erro))
                    if saida:
                        print(f"Saída de {ip}:\n{saida}")
                    if erro:
                        print(f"Erro em {ip}:\n{erro}")
                caminho_log = salvar_log(comando, resultados)
                print(f"\nLog salvo em: {caminho_log}")
            case "2":
                usuario = input("Usuário SSH: ")
                senha = input("Senha SSH: ")
                comando = input("Comando a executar: ")
                inicio_ip = 136
                fim_ip = 171
                resultados = []
                for ip in gerar_ips(inicio_ip, fim_ip):
                    print(f"Executando em {ip}...")
                    saida, erro = executar_comando_ssh(ip, usuario, senha, comando)
                    resultados.append((ip, saida, erro))
                    if saida:
                        print(f"Saída de {ip}:\n{saida}")
                    if erro:
                        print(f"Erro em {ip}:\n{erro}")
                caminho_log = salvar_log(comando, resultados)
                print(f"\nLog salvo em: {caminho_log}")
            case "3":
                usuario = input("Usuário WinRM: ")
                senha = input("Senha WinRM: ")
                comando = input("Comando a executar: ")
                inicio_ip = 172
                fim_ip = 175
                resultados = []
                for ip in gerar_ips(inicio_ip, fim_ip):
                    print(f"Executando em {ip}...")
                    saida, erro = executar_comando_winrm(ip, usuario, senha, comando)
                    resultados.append((ip, saida, erro))
                    if saida:
                        print(f"Saída de {ip}:\n{saida}")
                    if erro:
                        print(f"Erro em {ip}:\n{erro}")
                caminho_log = salvar_log(comando, resultados)
                print(f"\nLog salvo em: {caminho_log}")
            case "4":
                print("Saindo...")
                return
            case _:
                print("Opção inválida.")


if __name__ == "__main__":
    main()
