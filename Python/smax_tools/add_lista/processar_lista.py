# pip install unidecode

import requests
import unidecode
import json
import re
import os

from bs4 import BeautifulSoup

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)
caminho_config = os.path.join(diretorio_pai, 'config.json')
with open(caminho_config, 'r') as config_file:
    config = json.load(config_file)

def extrair_opcoes_motivo(html_content, tipo_contato):
  """Extrai as opções de 'Motivo do Contato' do HTML.

  Args:
    html_content: O conteúdo HTML da página.
    tipo_contato: O tipo de contato, 'denuncia' ou 'reclamacao'.

  Returns:
    Uma lista com as opções de 'Motivo do Contato'.
  """
  soup = BeautifulSoup(html_content, 'html.parser')
  select_id = f"select-{tipo_contato}-motivo-contato"
  select_element = soup.find('select', id=select_id)
  opcoes = [option.text.strip() for option in select_element.find_all('option')[1:]]
  return opcoes

def salvar_opcoes_em_arquivo(opcoes, nome_arquivo):
  """Salva as opções em um arquivo.

  Args:
    opcoes: Uma lista com as opções a serem salvas.
    nome_arquivo: O nome do arquivo a ser criado.
  """
  with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
    for i, opcao in enumerate(opcoes):
      if i > 0:
        arquivo.write('\n')
      arquivo.write(opcao)

def processar_linha(linha):
    linha_processada = unidecode.unidecode(linha)
    linha_processada = re.sub(r'[()./-]', '', linha_processada)
    palavras = linha_processada.split()
    palavras = [palavra for palavra in palavras if not palavra.islower()]
    linha_processada = ''.join(palavras)
    resultado = f"{linha_processada};{linha}"
    return resultado

def gerar_novos_itens(arquivo_ref, arquivo_saida):
  """Processa as linhas de um arquivo de referência e salva em um novo arquivo.

  Args:
    arquivo_ref: O nome do arquivo de referência (ex: 'ref_denuncia.txt').
    arquivo_saida: O nome do arquivo de saída (ex: 'novos_itens_denuncia.txt').
  """
  with open(arquivo_ref, 'r', encoding='utf-8') as arquivo:
    linhas = arquivo.readlines()

  linhas_processadas = [processar_linha(linha.strip()) for linha in linhas]

  with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
    for i, linha in enumerate(linhas_processadas):
      if i > 0:
        arquivo.write('\n')
      arquivo.write(linha)

  print(f"Arquivo '{arquivo_saida}' criado com sucesso.")

if __name__ == "__main__":
  url = config['url']
  response = requests.get(url)
  response.raise_for_status()

  opcoes_denuncia = extrair_opcoes_motivo(response.content, 'denuncia')
  opcoes_reclamacao = extrair_opcoes_motivo(response.content, 'reclamacao')

  salvar_opcoes_em_arquivo(opcoes_denuncia, 'ref_denuncia.txt')
  salvar_opcoes_em_arquivo(opcoes_reclamacao, 'ref_reclamacao.txt')

  gerar_novos_itens('ref_denuncia.txt', 'novos_itens_denuncia.txt')
  gerar_novos_itens('ref_reclamacao.txt', 'novos_itens_reclamacao.txt')