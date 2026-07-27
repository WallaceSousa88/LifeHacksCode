# pip install yt-dlp

import os
import sys
import yt_dlp

def obter_pasta_musicas() -> str:

    pasta = os.path.join(os.path.expanduser('~'), 'Music')
    if not os.path.isdir(pasta):
        print(f"Diretório de música não encontrado: {pasta}")
        sys.exit(1)
    return pasta

def baixar_musica(url: str, pasta_destino: str) -> None:

    if not url:
        print("Erro: Nenhuma URL foi fornecida.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nDownload concluído com sucesso!")
    except yt_dlp.utils.DownloadError as e:
        print(f"\nErro ao baixar o vídeo: verifique a URL ou a conexão.\nDetalhes: {e}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante o download: {e}")

def renomear_arquivos(pasta: str) -> None:

    AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.wav', '.webm', '.flac', '.ogg'}

    arquivos = [
        f for f in os.listdir(pasta)
        if os.path.isfile(os.path.join(pasta, f)) and os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
    ]
    arquivos.sort()

    if not arquivos:
        print("Nenhum arquivo de áudio encontrado para renomear.")
        return

    arquivos_renomeados = 0
    for i, nome_atual in enumerate(arquivos):
        extensao = os.path.splitext(nome_atual)[1]
        novo_nome = f"{i:03}{extensao}"
        caminho_antigo = os.path.join(pasta, nome_atual)
        caminho_novo = os.path.join(pasta, novo_nome)

        if caminho_antigo == caminho_novo:
            continue

        try:
            os.rename(caminho_antigo, caminho_novo)
            arquivos_renomeados += 1
        except PermissionError:
            print(f"Erro de permissão ao renomear '{nome_atual}'. Arquivo possivelmente aberto em outro programa.")
        except Exception as e:
            print(f"⚠️ Erro ao renomear '{nome_atual}': {e}")

    if arquivos_renomeados:
        print(f"\n Sucesso! {arquivos_renomeados} arquivos foram renomeados.")
    else:
        print("\n Nenhum arquivo precisou ser renomeado ou todos falharam.")

def menu_interativo() -> None:

    pasta = obter_pasta_musicas()
    while True:
        print("\n=== Gerenciador de Músicas ===")
        print("1) Baixar áudio do YouTube")
        print("2) Renomear arquivos de áudio (organizar)")
        print("3) Sair")
        escolha = input("Escolha uma opção (1/2/3): ").strip()

        if escolha == '1':
            url = input("Digite a URL do vídeo do YouTube que deseja baixar: ").strip()
            baixar_musica(url, pasta)
        elif escolha == '2':
            renomear_arquivos(pasta)
        elif escolha == '3':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")

if __name__ == "__main__":
    menu_interativo()