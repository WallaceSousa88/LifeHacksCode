import os

folder = r"C:\Users\Sky\Music"
files = os.listdir(folder)
files.sort()

for i, filename in enumerate(files):
    extension = os.path.splitext(filename)[1]
    new_name = f"{i:03}{extension}"
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)

print("Arquivos renomeados!")