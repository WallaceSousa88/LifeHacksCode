"""
Antes de executar este script, certifique-se de que tem o python 3.6+ instalado e que as seguintes bibliotecas Python estejam instaladas:

- selenium
- pyautogui
- python-docx
- pillow
- pyscreeze

Você pode instalar todas de uma vez com o seguinte comando:

pip install selenium pyautogui python-docx pillow pyscreeze

Além disso, este script requer o driver do Selenium. Você pode baixá-lo no seguinte site:

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

Depois de baixar o driver, coloque-o no seguinte diretório:

C:\\edgedriver_win64\\
"""

import os
import ast
import glob
import math
import shutil

def calculate_sleep_time(script_name):
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

def execute_script(script_name, user_id):
    os.system(f'python {script_name} {user_id}')

def remove_csv(user_id):
    files = glob.glob(f'C:\\Users\\{user_id}\\Downloads\\auditLog*.csv')    
    for file in files:
        os.remove(file)

def copiar_csv(user_id):
    shutil.copy(f'C:\\Users\\{user_id}\\Downloads\\auditLog.csv', f'C:\\Users\\{user_id}\\Desktop\\Relatorio\\')

def main():
    user_id = input("Digite sua matrícula: ")
    scripts = ['TI.AC.0092.py', 'TI.AC.0093.py', 'TI.MUD.0052.py', 'TI.MUD.0059.py']
    while True:
        print("Escolha uma opção:")
        for i, script in enumerate(scripts, 1):
            print(f"{i}. Executar o relatorio {script}. ~ {calculate_sleep_time(script)} min")
        print(f"{len(scripts) + 1}. Executar todos os relatórios. ~ {sum(calculate_sleep_time(script) for script in scripts)} min")
        print(f"{len(scripts) + 2}. Sair.")
        
        choice = input("Digite sua escolha: ")
        
        if choice == '1':
            remove_csv(user_id)
            execute_script('TI.AC.0092.py', user_id)
            copiar_csv(user_id)
        elif choice == '2':
            remove_csv(user_id)
            execute_script('TI.AC.0093.py', user_id)
            copiar_csv(user_id)
        elif choice == '3':
            remove_csv(user_id)
            execute_script('TI.MUD.0052.py', user_id)
            copiar_csv(user_id)
        elif choice == '4':
            remove_csv(user_id)
            execute_script('TI.MUD.0059.py', user_id)
            copiar_csv(user_id)
        elif choice == str(len(scripts) + 1):
            remove_csv(user_id)
            for script in scripts:
                execute_script(script, user_id)
            copiar_csv(user_id)
        elif choice == str(len(scripts) + 2):
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção.")

if __name__ == "__main__":
    main()
