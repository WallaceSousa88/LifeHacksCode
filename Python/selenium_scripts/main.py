import os
import ast
import glob
import math
import shutil
import sys

from pathlib import Path

def calcular_tempo_espera(nome_script):
    """
    Calcula o tempo total de espera em minutos de um script Python.

    Args:
        nome_script (str): O nome do script Python a ser analisado.

    Returns:
        int: O tempo total de espera em minutos.
    """
    with open(nome_script, 'r') as arquivo:
        arvore = ast.parse(arquivo.read())
    tempo_espera_total = 0
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute) and no.func.attr == 'sleep':
            tempo_espera_total += no.args[0].value
        elif isinstance(no, ast.Assign) and no.targets[0].id == 'tempo_rolagem':
            tempo_espera_total += no.value.value
    return math.ceil(tempo_espera_total / 60)

def executar_script(nome_script, id_usuario, unidade_disco):
    """
    Executa um script Python.

    Args:
        nome_script (str): O nome do script Python a ser executado.
        id_usuario (str): O ID do usuário.
        unidade_disco (str): A letra da unidade de disco.
    """
    caminho_documento = Path(f"{unidade_disco}:\\Users\\{id_usuario}\\Desktop\\Relatorio\\{nome_script.replace('.py', '.docx')}")
    if not caminho_documento.exists():
        print(f"Erro: O arquivo {caminho_documento} não foi encontrado.")
        print("Por favor, verifique se o arquivo existe no diretório especificado.")
        sys.exit(1)
    status = os.system(f'python {nome_script} {id_usuario} {unidade_disco}')
    if status != 0:
        print("Erro: Ocorreu um erro ao tentar executar o script.")
        print("Por favor, verifique os seguintes requisitos:")
        print("1. Driver Selenium instalado/atualizado na raiz da unidade em que for executado.")
        print("2. Python 3.6 ou superior instalado.")
        print("3. As seguintes bibliotecas Python instaladas: selenium, pyautogui, python-docx, pillow, pyscreeze.")
        print('4. Uma pasta com o nome "Relatorio" no desktop da unidade em que for executado com os arquivos de modelo .docx.')
        sys.exit(1)

def remover_csv(id_usuario, unidade_disco):
    """
    Remove todos os arquivos CSV com nome "auditLog*.csv" da pasta Downloads do usuário.

    Args:
        id_usuario (str): O ID do usuário.
        unidade_disco (str): A letra da unidade de disco.
    """
    arquivos = glob.glob(f'{unidade_disco}:\\Users\\{id_usuario}\\Downloads\\auditLog*.csv')
    for arquivo in arquivos:
        try:
            os.remove(arquivo)
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado. Continuando...")
            continue

def remover_json(id_usuario, unidade_disco):
    """
    Remove todos os arquivos JSON com nome "auditLog*.json" da pasta Downloads do usuário.

    Args:
        id_usuario (str): O ID do usuário.
        unidade_disco (str): A letra da unidade de disco.
    """
    arquivos = glob.glob(f'{unidade_disco}:\\Users\\{id_usuario}\\Downloads\\auditLog*.json')
    for arquivo in arquivos:
        try:
            os.remove(arquivo)
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado. Continuando...")
            continue

def copiar_csv(id_usuario, unidade_disco):
    """
    Copia o arquivo "auditLog.csv" da pasta Downloads do usuário para a pasta "Relatorio" na área de trabalho.

    Args:
        id_usuario (str): O ID do usuário.
        unidade_disco (str): A letra da unidade de disco.
    """
    try:
        shutil.copy(f'{unidade_disco}:\\Users\\{id_usuario}\\Downloads\\auditLog.csv', f'{unidade_disco}:\\Users\\{id_usuario}\\Desktop\\Relatorio\\')
    except FileNotFoundError:
        print("Arquivo auditLog.csv não encontrado. Continuando...")

def copiar_json(id_usuario, unidade_disco):
    """
    Copia o arquivo "auditLog.json" da pasta Downloads do usuário para a pasta "Relatorio" na área de trabalho.

    Args:
        id_usuario (str): O ID do usuário.
        unidade_disco (str): A letra da unidade de disco.
    """
    try:
        shutil.copy(f'{unidade_disco}:\\Users\\{id_usuario}\\Downloads\\auditLog.json', f'{unidade_disco}:\\Users\\{id_usuario}\\Desktop\\Relatorio\\')
    except FileNotFoundError:
        print("Arquivo auditLog.json não encontrado. Continuando...")

def exibir_ajuda():
    """
    Exibe a ajuda do programa.
    """
    print("Este programa automatiza a geração de relatórios.")
    print("Para usá-lo, siga estas etapas:")
    print("1. Certifique-se de ter as bibliotecas necessárias instaladas (selenium, pyautogui, python-docx, pillow, pyscreeze).")
    print("2. Tenha o driver Selenium compatível com seu navegador instalado e na pasta raiz da unidade em que for executar o programa.")
    print("3. Digite sua matrícula quando solicitado.")
    print("4. Digite a letra da unidade de disco onde seus arquivos estão localizados (por exemplo, C, D).")
    print("5. Escolha o relatório que deseja gerar a partir da lista.")
    print("6. O programa irá gerar o relatório e salvá-lo na pasta 'Relatorio' em sua área de trabalho.")

def main():
    """
    Função principal do programa.
    """
    if '-h' in sys.argv:
        exibir_ajuda()
        sys.exit(0)

    id_usuario = input("Digite sua matrícula: ")
    unidade_disco = input("Digite a letra da unidade do disco: ")
    scripts = ['TI.AC.0092.py', 'TI.AC.0093.py', 'TI.AC.0097.py', 'TI.MUD.0052.py', 'TI.MUD.0059.py']
    while True:
        print("Escolha uma opção:")
        for i, script in enumerate(scripts, 1):
            print(f"{i}. Executar o relatorio {script}. ~ {calcular_tempo_espera(script)} min")
        print(f"{len(scripts) + 1}. Executar todos os relatórios. ~ {sum(calcular_tempo_espera(script) for script in scripts)} min")
        print(f"{len(scripts) + 2}. Sair.")

        escolha = input("Digite sua escolha: ")

        if escolha == '1':
            remover_csv(id_usuario, unidade_disco)
            remover_json(id_usuario, unidade_disco)
            executar_script('TI.AC.0092.py', id_usuario, unidade_disco)
            copiar_csv(id_usuario, unidade_disco)
            copiar_json(id_usuario, unidade_disco)
        elif escolha == '2':
            remover_csv(id_usuario, unidade_disco)
            remover_json(id_usuario, unidade_disco)
            executar_script('TI.AC.0093.py', id_usuario, unidade_disco)
            copiar_csv(id_usuario, unidade_disco)
            copiar_json(id_usuario, unidade_disco)
        elif escolha == '3':
            remover_csv(id_usuario, unidade_disco)
            remover_json(id_usuario, unidade_disco)
            executar_script('TI.AC.0097.py', id_usuario, unidade_disco)
            copiar_csv(id_usuario, unidade_disco)
            copiar_json(id_usuario, unidade_disco)
        elif escolha == '4':
            remover_csv(id_usuario, unidade_disco)
            remover_json(id_usuario, unidade_disco)
            executar_script('TI.MUD.0052.py', id_usuario, unidade_disco)
            copiar_csv(id_usuario, unidade_disco)
            copiar_json(id_usuario, unidade_disco)
        elif escolha == '5':
            remover_csv(id_usuario, unidade_disco)
            remover_json(id_usuario, unidade_disco)
            executar_script('TI.MUD.0059.py', id_usuario, unidade_disco)
            copiar_csv(id_usuario, unidade_disco)
            copiar_json(id_usuario, unidade_disco)
        elif escolha == str(len(scripts) + 1):
            remover_csv(id_usuario, unidade_disco)
            remover_json(id_usuario, unidade_disco)
            for script in scripts:
                executar_script(script, id_usuario, unidade_disco)
            copiar_csv(id_usuario, unidade_disco)
            copiar_json(id_usuario, unidade_disco)
        elif escolha == str(len(scripts) + 2):
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção.")

if __name__ == "__main__":
    main()