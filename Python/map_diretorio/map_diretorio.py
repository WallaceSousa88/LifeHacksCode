import os

def listar_arquivos(caminho, nivel=0):
    for item in os.listdir(caminho):
        espacos = ' ' * nivel
        item_caminho = os.path.join(caminho, item)
        if os.path.isfile(item_caminho):
            yield f'{espacos}- {item}\n'
        else:
            yield f'{espacos}+ {item}\n'
            yield from listar_arquivos(item_caminho, nivel + 2)

def salvar_em_txt(caminho):
    nome_arquivo = os.path.basename(caminho) + '.txt'
    caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo)  
    with open(caminho_area_trabalho, 'w') as f:
        for linha in listar_arquivos(caminho):
            f.write(linha)

caminho = input("Digite o caminho do diretório que você deseja mapear: ")
salvar_em_txt(caminho)

print(f"Lista de arquivos salva em: {os.path.join(os.path.expanduser('~'), 'Desktop')}")
