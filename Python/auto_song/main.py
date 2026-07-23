import os

folder = os.path.join(os.path.expanduser('~'), 'Music')
AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.wav', '.webm', '.flac', '.ogg'}

files = [
    f for f in os.listdir(folder)
    if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
]
files.sort()

if not files:
    print("Nenhum arquivo de áudio encontrado para renomear.")
    exit()

for i, filename in enumerate(files):
    extension = os.path.splitext(filename)[1]
    new_name = f"{i:03}{extension}"
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)

print("Arquivos renomeados!")