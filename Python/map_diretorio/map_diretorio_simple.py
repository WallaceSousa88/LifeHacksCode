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
    try:
        with open(caminho_area_trabalho, 'w') as f:
            for linha in listar_arquivos(caminho):
                f.write(linha)
        print(f"Lista de arquivos salva em: {caminho_area_trabalho}")
    except PermissionError:
        print(f"Erro: Permissão negada para escrever em: {caminho_area_trabalho}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

def main():
    caminho = input("Digite o caminho do diretório que você deseja mapear: ")
    if os.path.isdir(caminho):
        salvar_em_txt(caminho)
    else:
        print("Erro: Caminho inválido ou não é um diretório.")

if __name__ == "__main__":
    main()