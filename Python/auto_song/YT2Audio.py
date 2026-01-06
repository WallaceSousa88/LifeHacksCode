# pip install yt-dlp

import yt_dlp

url = "x"

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': r'C:\Users\Sky\Music\%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download concluído !")