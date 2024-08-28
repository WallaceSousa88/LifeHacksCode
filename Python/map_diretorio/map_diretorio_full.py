import os

def listar_arquivos(caminho, ignorar_pastas=None):
    if ignorar_pastas is None:
        ignorar_pastas = []
    for root, dirs, files in os.walk(caminho):
        # Remove as pastas a serem ignoradas
        dirs[:] = [d for d in dirs if d not in ignorar_pastas]
        for file in files:
            yield os.path.relpath(os.path.join(root, file), caminho)

def obter_conteudo_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo não encontrado: '{caminho_arquivo}'"
    except PermissionError:
        return f"Erro: Permissão negada para ler o arquivo: '{caminho_arquivo}'"
    except Exception as e:
        return f"Erro ao ler o arquivo '{caminho_arquivo}': {e}"

def gerar_relatorio(caminho, arquivos_conteudo=None, ignorar_pastas=None):
    relatorio = f"Relatório da estrutura do diretório '{caminho}':\n\nEstrutura:\n"
    for linha in listar_arquivos(caminho, ignorar_pastas):
        relatorio += f"{linha}\n"

    if arquivos_conteudo:
        relatorio += "\nConteúdo dos arquivos:\n"
        for arquivo in arquivos_conteudo:
            caminho_arquivo = os.path.join(caminho, arquivo)
            conteudo = obter_conteudo_arquivo(caminho_arquivo) 
            relatorio += f"\nO código do arquivo '{arquivo}' é:\n\n```\n{conteudo}\n```\n"
    
    return relatorio

def main():
    caminho = input("Digite o caminho do diretório que você deseja analisar: ")
    if os.path.isdir(caminho):
        arquivos_conteudo = []
        while True:
            arquivo_para_conteudo = input("Digite o nome do arquivo para incluir o conteúdo (ou pressione Enter para pular): ")
            if not arquivo_para_conteudo:
                break
            arquivos_conteudo.append(arquivo_para_conteudo)

        pastas_ignorar = []
        while True:
            pasta_ignorar = input("Digite o nome da pasta a ser ignorada (ou pressione Enter para continuar): ")
            if not pasta_ignorar:
                break
            pastas_ignorar.append(pasta_ignorar)

        relatorio = gerar_relatorio(caminho, arquivos_conteudo, pastas_ignorar)
        relatorio = relatorio.replace(f"considerando o diretório '{caminho}':", "")

        nome_arquivo = os.path.basename(caminho) + '_relatorio.txt'
        caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", nome_arquivo) 
        try:
            with open(caminho_area_trabalho, 'w', encoding='utf-8') as f:
                f.write(relatorio)
            print(f"Relatório salvo em: {caminho_area_trabalho}")
        except Exception as e:
            print(f"Erro ao salvar o relatório: {e}")

    else:
        print("Erro: Caminho inválido ou não é um diretório.")

if __name__ == "__main__":
    main()
