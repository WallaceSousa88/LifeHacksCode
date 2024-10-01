# pip install unidecode

import unidecode
import re

def processar_linha(linha):
    linha_processada = unidecode.unidecode(linha)

    linha_processada = re.sub(r'[()./-]', '', linha_processada)

    palavras = linha_processada.split()
    palavras = [palavra for palavra in palavras if not palavra.islower()]

    linha_processada = ''.join(palavras)

    resultado = f"{linha_processada};{linha}"

    return resultado

with open('ref.txt', 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()

linhas_processadas = [processar_linha(linha.strip()) for linha in linhas]

with open('novos_itens.txt', 'w', encoding='utf-8') as arquivo:
    for linha in linhas_processadas:
        arquivo.write(linha + '\n')

print("Arquivo novos_itens.txt criado com sucesso.")