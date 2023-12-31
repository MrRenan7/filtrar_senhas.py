import os
import random
import sys
import subprocess
import requests
from colorama import Fore, Style
from cryptography.fernet import Fernet

def gerar_chave():
    chave = Fernet.generate_key()
    with open('chave.key', 'wb') as chave_arquivo:
        chave_arquivo.write(chave)

def carregar_chave():
    with open('chave.key', 'rb') as chave_arquivo:
        chave = chave_arquivo.read()
    return chave

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

def criptografar_senhas():
    chave = carregar_chave()
    f = Fernet(chave)

    caminho_arquivo = os.path.expanduser("/root/senhas.txt")
    caminho_saida = os.path.expanduser("/root/senhas.crip.txt")

    if not validar_arquivo(caminho_arquivo):
        return

    with open(caminho_arquivo, 'r') as arquivo_entrada:
        senhas = arquivo_entrada.readlines()

    senhas_criptografadas = []
    for senha in senhas:
        senha = senha.strip().encode()
        senha_criptografada = f.encrypt(senha)
        senhas_criptografadas.append(senha_criptografada)

    with open(caminho_saida, 'wb') as arquivo_saida:
        for senha_criptografada in senhas_criptografadas:
            arquivo_saida.write(senha_criptografada + b'\n')

    print(f"{Fore.GREEN}Senhas criptografadas foram salvas no arquivo {caminho_saida}.{Style.RESET_ALL}")

def descriptografar_senhas():
    chave = carregar_chave()
    f = Fernet(chave)

    caminho_arquivo = os.path.expanduser("/root/senhas.crip.txt")
    caminho_saida = os.path.expanduser("/root/senhas_descriptografadas.txt")

    if not validar_arquivo(caminho_arquivo):
        return

    with open(caminho_arquivo, 'rb') as arquivo_entrada:
        senhas_criptografadas = arquivo_entrada.readlines()

    senhas_descriptografadas = []
    for senha_criptografada in senhas_criptografadas:
        senha_criptografada = senha_criptografada.strip()
        senha_descriptografada = f.decrypt(senha_criptografada)
        senhas_descriptografadas.append(senha_descriptografada.decode())

    with open(caminho_saida, 'w') as arquivo_saida:
        for senha_descriptografada in senhas_descriptografadas:
            arquivo_saida.write(senha_descriptografada + '\n')

    print(f"{Fore.GREEN}Senhas descriptografadas foram salvas no arquivo {caminho_saida}.{Style.RESET_ALL}")

def exibir_menu():
    while True:
        print(f"{Fore.CYAN}{Style.BRIGHT}╔═══════════════════ MENU ═════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [01] • Filtrar senhas de 4 dígitos       ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [02] • Filtrar senhas de 8 dígitos       ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [03] • Filtrar senhas de 10 dígitos      ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [04] • Filtrar senhas de 12 dígitos      ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [05] • Gerar senhas aleatórias (Seguras) ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [06] • Verificar força da senha          ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [07] • Atualizar código                  ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [08] • Criptografar senhas               ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [09] • Descriptografar senhas            ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [10] • Gerar chave                       ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ [00] • Sair                              ║{Style.RESET_ALL}")
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
            atualizar_codigo()
        elif opcao == "8":
            criptografar_senhas()
        elif opcao == "9":
            descriptografar_senhas()
        elif opcao == "10":
            gerar_chave()
        elif opcao == "0":
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

exibir_menu()
