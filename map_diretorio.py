import os
import sys

def listar_arquivos(caminho, nivel=0):
    for item in os.listdir(caminho):
        espacos = ' ' * nivel
        if os.path.isfile(os.path.join(caminho, item)):
            print(f'{espacos}- {item}')
        else:
            print(f'{espacos}+ {item}')
            listar_arquivos(os.path.join(caminho, item), nivel + 2)

def salvar_em_txt(caminho, arquivo_saida):
    original_stdout = sys.stdout
    with open(arquivo_saida, 'w') as f:
        sys.stdout = f
        listar_arquivos(caminho)
        sys.stdout = original_stdout

caminho = input("Digite o caminho do diretório que você deseja mapear: ")
arquivo_saida = input("Digite o caminho do arquivo onde você deseja salvar a lista de arquivos: ")

salvar_em_txt(caminho, arquivo_saida)
