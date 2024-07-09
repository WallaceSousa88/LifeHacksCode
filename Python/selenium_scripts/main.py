import os
import ast
import glob
import math
import shutil
import sys
from pathlib import Path

def calc_sleep_time(script_name):
    with open(script_name, 'r') as file:
        tree = ast.parse(file.read())
    total_sleep_time = sum(node.args[0].value for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'sleep')
    total_sleep_time_in_minutes = math.ceil(total_sleep_time / 60)
    scroll_time = next((node.value.value for node in ast.walk(tree) if isinstance(node, ast.Assign) and node.targets[0].id == 'scroll_time'), None)
    if scroll_time is not None:
        scroll_time_in_minutes = math.ceil(scroll_time / 60)
    else:
        scroll_time_in_minutes = 0
    return total_sleep_time_in_minutes + scroll_time_in_minutes

def execute_script(script_name, user_id, unidade_disco):
    doc_path = Path(f"{unidade_disco}:\\Users\\{user_id}\\Desktop\\Relatorio\\{script_name.replace('.py', '.docx')}")
    if not doc_path.exists():
        print(f"Erro: O arquivo {doc_path} não foi encontrado.")
        print("Por favor, verifique se o arquivo existe no diretório especificado.")
        sys.exit(1)
    status = os.system(f'python {script_name} {user_id} {unidade_disco}')
    if status != 0:
        print("Erro: Ocorreu um erro ao tentar executar o script.")
        print("Por favor, verifique os seguintes requisitos:")
        print("1. Driver Selenium instalado/atualizado na raiz da unidade em que for executado.")
        print("2. Python 3.6 ou superior instalado.")
        print("3. As seguintes bibliotecas Python instaladas: selenium, pyautogui, python-docx, pillow, pyscreeze.")
        print('4. Uma pasta com o nome "Relatorio" no desktop da unidade em que for executado com os arquivos de modelo .docx.')
        sys.exit(1)

def remove_csv(user_id, unidade_disco):
    files = glob.glob(f'{unidade_disco}:\\Users\\{user_id}\\Downloads\\auditLog*.csv')
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f"Arquivo {file} não encontrado. Continuando...")
            continue

def copiar_csv(user_id, unidade_disco):
    try:
        shutil.copy(f'{unidade_disco}:\\Users\\{user_id}\\Downloads\\auditLog.csv', f'{unidade_disco}:\\Users\\{user_id}\\Desktop\\Relatorio\\')
    except FileNotFoundError:
        print("Arquivo auditLog.csv não encontrado. Continuando...")

def main():
    user_id = input("Digite sua matrícula: ")
    unidade_disco = input("Digite a letra da unidade do disco: ")
    scripts = ['TI.AC.0092.py', 'TI.AC.0093.py', 'TI.AC.0097.py', 'TI.MUD.0052.py', 'TI.MUD.0059.py']
    while True:
        print("Escolha uma opção:")
        for i, script in enumerate(scripts, 1):
            print(f"{i}. Executar o relatorio {script}. ~ {calc_sleep_time(script)} min")
        print(f"{len(scripts) + 1}. Executar todos os relatórios. ~ {sum(calc_sleep_time(script) for script in scripts)} min")
        print(f"{len(scripts) + 2}. Sair.")
        
        choice = input("Digite sua escolha: ")
        
        if choice == '1':
            remove_csv(user_id, unidade_disco)
            execute_script('TI.AC.0092.py', user_id, unidade_disco)
            copiar_csv(user_id, unidade_disco)
        elif choice == '2':
            remove_csv(user_id, unidade_disco)
            execute_script('TI.AC.0093.py', user_id, unidade_disco)
            copiar_csv(user_id, unidade_disco)
        elif choice == '3':
            remove_csv(user_id, unidade_disco)
            execute_script('TI.AC.0097.py', user_id, unidade_disco)
            copiar_csv(user_id, unidade_disco)
        elif choice == '4':
            remove_csv(user_id, unidade_disco)
            execute_script('TI.MUD.0052.py', user_id, unidade_disco)
            copiar_csv(user_id, unidade_disco)
        elif choice == '5':
            remove_csv(user_id, unidade_disco)
            execute_script('TI.MUD.0059.py', user_id, unidade_disco)
            copiar_csv(user_id, unidade_disco)
        elif choice == str(len(scripts) + 1):
            remove_csv(user_id, unidade_disco)
            for script in scripts:
                execute_script(script, user_id, unidade_disco)
            copiar_csv(user_id, unidade_disco)
        elif choice == str(len(scripts) + 2):
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção.")

if __name__ == "__main__":
    main()
