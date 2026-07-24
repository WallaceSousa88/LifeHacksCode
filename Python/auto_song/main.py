import os

folder = os.path.join(os.path.expanduser('~'), 'Music')
if not os.path.isdir(folder):
    print(f"Diretório de música não encontrado: {folder}")
    exit()

AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.wav', '.webm', '.flac', '.ogg'}

files = [
    f for f in os.listdir(folder)
    if os.path.isfile(os.path.join(folder, f)) and os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
]
files.sort()

if not files:
    print("Nenhum arquivo de áudio encontrado para renomear.")
    exit()

arquivos_renomeados = 0
for i, filename in enumerate(files):
    extension = os.path.splitext(filename)[1]
    new_name = f"{i:03}{extension}"
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)

    if old_path == new_path:
        continue

    try:
        os.rename(old_path, new_path)
        arquivos_renomeados += 1
    except PermissionError:
        print(f"Erro de permissão: não foi possível renomear '{filename}'. O arquivo pode estar aberto em outro programa.")
    except Exception as e:
        print(f"Erro ao renomear '{filename}': {e}")

if arquivos_renomeados > 0:
    print(f"Sucesso! {arquivos_renomeados} arquivos renomeados.")
else:
    print("Nenhum arquivo precisou ser renomeado ou ocorreu algum erro.")