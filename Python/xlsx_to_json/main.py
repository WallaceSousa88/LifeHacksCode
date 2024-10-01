# pip install pandas openpyxl

import pandas as pd
import os
import json

def converter_xlsx_para_json(pasta_xlsx, pasta_json):
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

if __name__ == "__main__":
  pasta_xlsx = "xlsx"
  pasta_json = "json"
  converter_xlsx_para_json(pasta_xlsx, pasta_json)