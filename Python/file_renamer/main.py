# permutation
# n! / (n - r)!
# 100! / (100 - 3)! = 100! / 97! = 100 * 99 * 98 = 970.200

import os
import random

def carregar_palavras_do_arquivo(nome_do_arquivo):
    with open(nome_do_arquivo, 'r', encoding='utf-8') as arquivo:
        return [linha.strip() for linha in arquivo if linha.strip()]

def gerar_novo_nome(palavras, extensao_arquivo):
    return '_'.join(random.sample(palavras, k=min(3, len(palavras)))) + extensao_arquivo

def renomear_arquivos(caminho_da_pasta):
    nome_do_arquivo_de_palavras = 'example.txt'
    lista_de_palavras = carregar_palavras_do_arquivo(nome_do_arquivo_de_palavras)

    for arquivo in os.listdir(caminho_da_pasta):
        caminho_completo_antigo = os.path.join(caminho_da_pasta, arquivo)

        if not os.path.isfile(caminho_completo_antigo):
            continue

        _, extensao_arquivo = os.path.splitext(arquivo)
        novo_nome = gerar_novo_nome(lista_de_palavras, extensao_arquivo)
        caminho_completo_novo = os.path.join(caminho_da_pasta, novo_nome)

        if os.path.exists(caminho_completo_novo):
            print(f"O arquivo {novo_nome} já existe.")
            continue

        os.rename(caminho_completo_antigo, caminho_completo_novo)

if __name__ == "__main__":
    caminho_da_pasta = input("Digite o caminho da pasta: ")
    renomear_arquivos(caminho_da_pasta)