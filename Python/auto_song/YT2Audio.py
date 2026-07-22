# pip install yt-dlp

import os
import yt_dlp

url = input("Digite a URL do vídeo que deseja baixar: ").strip()

if not url:
    print("Erro: Nenhuma URL foi fornecida. Encerrando...")
    exit()

pasta_musicas = os.path.join(os.path.expanduser('~'), 'Music')

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(pasta_musicas, '%(title)s.%(ext)s'),
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download concluído !")