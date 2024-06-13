import os

def listar_arquivos(caminho, nivel=0):
    for item in os.listdir(caminho):
        espacos = ' ' * nivel
        if os.path.isfile(os.path.join(caminho, item)):
            yield f'{espacos}- {item}\n'
        else:
            yield f'{espacos}+ {item}\n'
            yield from listar_arquivos(os.path.join(caminho, item), nivel + 2)

def salvar_em_txt(caminho, arquivo_saida):
    with open(arquivo_saida, 'w') as f:
        for linha in listar_arquivos(caminho):
            f.write(linha)

caminho = input("Digite o caminho do diretório que você deseja mapear: ")
arquivo_saida = input("Digite o caminho do arquivo onde você deseja salvar a lista de arquivos: ")

salvar_em_txt(caminho, arquivo_saida)
