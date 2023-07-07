import os
import random
import sys
import subprocess
import psutil
import requests
from colorama import Fore, Style

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def info_sistema():
    # Obtendo informações do sistema operacional
    system_info = run_command("lsb_release -a")
    kernel_version = run_command("uname -r")
    virtualization = run_command("systemd-detect-virt")
    architecture = run_command("uname -m")

    # Obtendo informações do processador
    processor_model = run_command("cat /proc/cpuinfo | grep 'model name' | uniq | cut -d ':' -f 2")
    num_cores = run_command("nproc")
    cache_size = run_command("lscpu | grep 'L3 cache' | cut -d ':' -f 2 | awk '{print $1,$2}'")
    cpu_usage = run_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")

    # Obtendo informações da memória RAM
    memory_info = run_command("free -h")
    memory_lines = memory_info.split('\n')
    total_memory = ""
    free_memory = ""
    cached_memory = ""
    ram_usage = ""

    if len(memory_lines) > 2:
        total_memory = memory_lines[1].split()[1]
        free_memory = memory_lines[2].split()[3]
        if len(memory_lines[2].split()) > 5:
            cached_memory = memory_lines[2].split()[5]
        ram_usage = memory_lines[2].split()[2]

    # Obtendo serviços em execução e suas portas
    services = {
        'v2ray': [],
        'plugin-bo': [],
        'sshd': [],
        'stunnel4': [],
        'check_use': [],
        'badvpn-ud': [],
        'python': [],
        'nginx': []
    }

    for conn in psutil.net_connections():
        if conn.status == "LISTEN":
            for service, ports in services.items():
                if conn.laddr.port in ports:
                    services[service].append(conn.laddr.port)

    # Retornando as informações coletadas
    informacoes = {
        'Sistema Operacional': {
            'Informação': system_info,
            'Kernel': kernel_version,
            'Virtualização': virtualization,
            'Arquitetura': architecture
        },
        'Processador': {
            'Modelo': processor_model,
            'Núcleos': num_cores,
            'Memória Cache': cache_size,
            'Utilização': cpu_usage + "%"
        },
        'Memória RAM': {
            'Total': total_memory,
            'Livre': free_memory,
            'Cache': cached_memory,
            'Utilização': ram_usage
        },
        'Serviços em Execução': services
    }

    return informacoes

def validar_arquivo(caminho_arquivo):
    if not os.path.isfile(caminho_arquivo):
        print(f"{Fore.RED}O arquivo de senhas não foi encontrado.{Style.RESET_ALL}")
        return False
    return True

def filtrar_senhas(caminho_arquivo, comprimento, caminho_saida):
    if not validar_arquivo(caminho_arquivo):
        return

    senhas_filtradas = []
    senhas_unicas = set()

    with open(caminho_arquivo, "r") as arquivo:
        for linha in arquivo:
            senha = linha.strip()
            if len(senha) == comprimento and senha.isalnum() and senha not in senhas_unicas:
                senhas_filtradas.append(senha)
                senhas_unicas.add(senha)

    with open(caminho_saida, "w") as arquivo_saida:
        for senha in senhas_filtradas:
            arquivo_saida.write(senha + "\n")

    print(f"{Fore.GREEN}Senhas filtradas foram salvas no arquivo {caminho_saida}.{Style.RESET_ALL}")

def filtrar_senhas_4_digitos():
    caminho_arquivo = os.path.expanduser("/root/senhas.txt")
    caminho_saida = os.path.expanduser("/root/senhas_filtradas_4.txt")
    filtrar_senhas(caminho_arquivo, 4, caminho_saida)

def filtrar_senhas_8_digitos():
    caminho_arquivo = os.path.expanduser("/root/senhas.txt")
    caminho_saida = os.path.expanduser("/root/senhas_filtradas_8.txt")
    filtrar_senhas(caminho_arquivo, 8, caminho_saida)

def filtrar_senhas_10_digitos():
    caminho_arquivo = os.path.expanduser("/root/senhas.txt")
    caminho_saida = os.path.expanduser("/root/senhas_filtradas_10.txt")
    filtrar_senhas(caminho_arquivo, 10, caminho_saida)

def filtrar_senhas_12_digitos():
    caminho_arquivo = os.path.expanduser("/root/senhas.txt")
    caminho_saida = os.path.expanduser("/root/senhas_filtradas_12.txt")
    filtrar_senhas(caminho_arquivo, 12, caminho_saida)

def gerar_senhas_aleatorias(comprimento, caracteres_especiais=False, numeros=False, letras_maiusculas=False, letras_minusculas=False, quantidade=1):
    caracteres_permitidos = ""
    if caracteres_especiais:
        caracteres_permitidos += "!@#$%^&*()_-+=<>?/\\"
    if numeros:
        caracteres_permitidos += "0123456789"
    if letras_maiusculas:
        caracteres_permitidos += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if letras_minusculas:
        caracteres_permitidos += "abcdefghijklmnopqrstuvwxyz"

    senhas_geradas = []

    for _ in range(quantidade):
        senha = ''.join(random.choice(caracteres_permitidos) for _ in range(comprimento))
        senhas_geradas.append(senha)

    caminho_saida = os.path.expanduser("/root/senhas_geradas.txt")

    with open(caminho_saida, "w") as arquivo_saida:
        for senha in senhas_geradas:
            arquivo_saida.write(senha + "\n")

    print(f"{Fore.GREEN}Senhas aleatórias geradas foram salvas no arquivo {caminho_saida}.{Style.RESET_ALL}")

def verificar_forca_senha(senha):
    forca = 0

    # Critério de comprimento mínimo
    if len(senha) >= 8:
        forca += 1

    # Critério de uso de caracteres especiais
    if any(char in "!@#$%^&*()-_=+[]{};:,.<>/?\\|`~" for char in senha):
        forca += 1

    # Critério de uso de letras maiúsculas e minúsculas
    if any(char.isupper() for char in senha) and any(char.islower() for char in senha):
        forca += 1

    # Critério de uso de números
    if any(char.isdigit() for char in senha):
        forca += 1

    return forca

def atualizar_codigo():
    url = "https://raw.githubusercontent.com/MrRenan7/filtrar-senhas/master/filtrar_senhas.py"
    response = requests.get(url)

    if response.status_code == 200:
        novo_codigo = response.text

        # Salvar o novo código em um novo arquivo
        with open("filtrar_senhas.py", "w") as arquivo:
            arquivo.write(novo_codigo)

        print("Código atualizado com sucesso.")

        # Reiniciar o script com o novo arquivo
        python = sys.executable
        subprocess.call([python, "filtrar_senhas.py"])
        sys.exit()

    else:
        print(f"Erro ao atualizar o código: {response.status_code}")

def exibir_menu():
    while True:
        print(f"{Fore.CYAN}{Style.BRIGHT}╔══════════════════ MENU ══════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [01] • Filtrar senhas de 4 dígitos       ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [02] • Filtrar senhas de 8 dígitos       ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [03] • Filtrar senhas de 10 dígitos      ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [04] • Filtrar senhas de 12 dígitos      ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [05] • Gerar senhas aleatórias           ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [06] • Verificar força da senha          ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [07] • Obter informações do sistema      ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [08] • Atualizar código                  ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [09] • Sair                              ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}╚══════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"{Fore.RED}Script made by @MrRenan7{Style.RESET_ALL}")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            filtrar_senhas_4_digitos()
        elif opcao == "2":
            filtrar_senhas_8_digitos()
        elif opcao == "3":
            filtrar_senhas_10_digitos()
        elif opcao == "4":
            filtrar_senhas_12_digitos()
        elif opcao == "5":
            comprimento = int(input("Informe o comprimento da senha: "))
            caracteres_especiais = input("Incluir caracteres especiais? (S/N): ").lower() == "s"
            numeros = input("Incluir números? (S/N): ").lower() == "s"
            letras_maiusculas = input("Incluir letras maiúsculas? (S/N): ").lower() == "s"
            letras_minusculas = input("Incluir letras minúsculas? (S/N): ").lower() == "s"
            quantidade = int(input("Quantidade de senhas a serem geradas: "))
            gerar_senhas_aleatorias(comprimento, caracteres_especiais, numeros, letras_maiusculas, letras_minusculas, quantidade)
        elif opcao == "6":
            senha = input("Digite a senha a ser verificada: ")
            forca_senha = verificar_forca_senha(senha)
            print(f"A força da senha é: {forca_senha}")
        elif opcao == "7":
            informacoes_sistema = info_sistema()

            # Exibir as informações do sistema
            for categoria, detalhes in informacoes_sistema.items():
                print(f"{Fore.CYAN}{Style.BRIGHT}║ {categoria:<41} ║{Style.RESET_ALL}")
                for chave, valor in detalhes.items():
                    print(f"{Fore.CYAN}{Style.BRIGHT}║   {chave:<37}{valor:<37}║{Style.RESET_ALL}")
        elif opcao == "8":
            atualizar_codigo()
        elif opcao == "9":
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

exibir_menu()
