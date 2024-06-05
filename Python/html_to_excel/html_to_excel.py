# pip install beautifulsoup4
# pip install pandas
# pip install openpyxl
# pip install beautifulsoup4 pandas openpyxl

from bs4 import BeautifulSoup
import re
import pandas as pd

def ler_html(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo_html = arquivo.read()
        return conteudo_html
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return None

def extrair_dados(conteudo_html):
    sopa = BeautifulSoup(conteudo_html, 'html.parser')
    divs_atualizacao = sopa.find_all('div', style='text-align:left;')

    lista_nomes_maquinas = []
    lista_ultimas_atualizacoes = []

    for div_atualizacao in divs_atualizacao:
        nome_maquina = div_atualizacao.find_previous('h2', class_='fs-4 fw-bold').get_text(strip=True)
        tag_ultima_atualizacao = div_atualizacao.find('p')
        
        if tag_ultima_atualizacao:
            ultima_atualizacao = tag_ultima_atualizacao.get_text(strip=True)
            ultima_atualizacao = re.sub(r'\.\d+', '', ultima_atualizacao)
            lista_nomes_maquinas.append(nome_maquina)
            lista_ultimas_atualizacoes.append(ultima_atualizacao)

    return lista_nomes_maquinas, lista_ultimas_atualizacoes

def salvar_excel(nomes_maquinas, ultimas_atualizacoes, caminho_saida):
    dados = {'Nome da Máquina': nomes_maquinas, 'Última Atualização': ultimas_atualizacoes}
    df = pd.DataFrame(dados)
    df.to_excel(caminho_saida, index=False)

def main():
    caminho_html = input('Digite o caminho do arquivo HTML: ')
    conteudo_html = ler_html(caminho_html)

    if conteudo_html:
        nomes_maquinas, ultimas_atualizacoes = extrair_dados(conteudo_html)
        caminho_saida = input('Digite o local de saída para o arquivo Excel: ')
        salvar_excel(nomes_maquinas, ultimas_atualizacoes, caminho_saida)
        print(f"Os resultados foram salvos em '{caminho_saida}'.")

if __name__ == "__main__":
    main()
