import os
import random

lista_de_palavras = ["String_1", "String_2", "String_3"]

caminho_da_pasta = r"C:\x"

arquivos = os.listdir(caminho_da_pasta)

for arquivo in arquivos:
    novas_palavras = random.sample(lista_de_palavras, 3)
    
    novo_nome = '_'.join(novas_palavras) + os.path.splitext(arquivo)[1]
    
    if os.path.exists(os.path.join(caminho_da_pasta, novo_nome)):
        print(f"O arquivo {novo_nome} já existe.")
        continue
    
    os.rename(os.path.join(caminho_da_pasta, arquivo), os.path.join(caminho_da_pasta, novo_nome))
