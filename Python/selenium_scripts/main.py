"""
Antes de executar este script, certifique-se de que tem o python 3+ instalado e que as seguintes bibliotecas Python estejam instaladas:

- selenium
- pyautogui
- python-docx
- pillow
- pyscreeze

pip install selenium pyautogui python-docx pillow pyscreeze

Além disso, este script requer o driver do Selenium. Você pode baixá-lo no seguinte site:

https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

Depois de baixar o driver, coloque-o no seguinte diretório:

C:\\edgedriver_win64\\
"""

import os
import glob
import shutil

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
    while True:
        print("Escolha uma opção:")
        print("1. Executar o relatorio TI.AC.0093.")
        print("2. Executar o relatorio TI.MUD.0052.")
        print("3. Executar o relatorio TI.MUD.0059.")
        print("4. Executar todos os relatórios.")
        print("5. Sair.")
        
        choice = input("Digite sua escolha: ")
        
        if choice == '1':
            remove_csv(user_id)
            execute_script('TI.AC.0093.py', user_id)
            copiar_csv(user_id)
        elif choice == '2':
            remove_csv(user_id)
            execute_script('TI.MUD.0052.py', user_id)
            copiar_csv(user_id)
        elif choice == '3':
            remove_csv(user_id)
            execute_script('TI.MUD.0059.py', user_id)
            copiar_csv(user_id)
        elif choice == '4':
            remove_csv(user_id)
            for script in ['TI.AC.0093.py', 'TI.MUD.0052.py', 'TI.MUD.0059.py']:
                execute_script(script, user_id)
            copiar_csv(user_id)
        elif choice == '5':
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção.")

if __name__ == "__main__":
    main()
