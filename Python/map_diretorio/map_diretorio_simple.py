import os

def listar_arquivos(caminho):
    for root, dirs, files in os.walk(caminho):
        for file in files:
            relpath = os.path.relpath(os.path.join(root, file), caminho)
            if os.path.dirname(relpath):
                yield f"\\{relpath}"
            else:
                yield relpath

def salvar_em_txt(caminho):
    nome_arquivo = os.path.basename(caminho) + '.txt'
    caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo)  
    try:
        with open(caminho_area_trabalho, 'w', encoding='utf-8') as f:
            f.write(f"O diretório base é '{caminho}'. Abaixo está a lista de arquivos e pastas a partir desse diretório:\n\n")
            for linha in listar_arquivos(caminho):
                f.write(linha + '\n')
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
