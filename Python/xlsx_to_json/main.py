# pip install pandas openpyxl

import pandas as pd
import os
import json

def xlsx_to_json(pasta_xlsx, pasta_json):
    for nome_arquivo in os.listdir(pasta_xlsx):
        if nome_arquivo.endswith(".xlsx"):
            caminho_arquivo_excel = os.path.join(pasta_xlsx, nome_arquivo)
            nome_arquivo_base = os.path.splitext(nome_arquivo)[0]
            caminho_arquivo_json = os.path.join(pasta_json, f"{nome_arquivo_base}.json")

            df = pd.read_excel(caminho_arquivo_excel)
            dados = df.to_dict(orient='records')

            for linha in dados:
                for coluna, valor in linha.items():
                    if isinstance(valor, pd.Timestamp):
                        linha[coluna] = valor.strftime("%Y-%m-%d")

            with open(caminho_arquivo_json, "w") as arquivo_json:
                json.dump(dados, arquivo_json, indent=4)

            tamanho_original = os.path.getsize(caminho_arquivo_excel) / 1024
            tamanho_novo = os.path.getsize(caminho_arquivo_json) / 1024
            diferenca_tamanho = tamanho_novo - tamanho_original

            print(f"Arquivo: {nome_arquivo}")
            print(f"Original: {tamanho_original:.2f} KB")
            print(f"Novo: {tamanho_novo:.2f} KB")

            if diferenca_tamanho > 0:
                aumento_percentual = (diferenca_tamanho / tamanho_original) * 100
                print(f"Relação: {aumento_percentual:.2f}% maior\n")
            elif diferenca_tamanho < 0:
                reducao_percentual = (-diferenca_tamanho / tamanho_original) * 100
                print(f"Relação: {reducao_percentual:.2f}% menor\n")
            else:
                print("Relação: Os arquivos têm o mesmo tamanho\n")

if __name__ == "__main__":
    pasta_xlsx = "in"
    pasta_json = "out"
    xlsx_to_json(pasta_xlsx, pasta_json)