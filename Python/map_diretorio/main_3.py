import os

def listar_arquivos(caminho):
    for root, dirs, files in os.walk(caminho):
        for file in files:
            yield os.path.join(root, file)

def salvar_em_txt(caminho):
    nome_arquivo = os.path.basename(caminho) + '.txt'
    caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo)
    try:
        with open(caminho_area_trabalho, 'w', encoding='utf-8') as f:
            f.write(f"O diretório base é '{caminho}'. Abaixo está a lista de arquivos e seus conteúdos a partir desse diretório:\n\n")
            for arquivo in listar_arquivos(caminho):
                f.write(f"Endereço completo do arquivo: {arquivo}\n")
                try:
                    with open(arquivo, 'r', encoding='utf-8') as file_content:
                        f.write(file_content.read() + '\n')
                except Exception as e:
                    f.write(f"Erro ao ler o arquivo: {e}\n")
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