import requests
from bs4 import BeautifulSoup

def encontrar_produto_amazon(nome_produto):
    """
    Pesquisa por um produto na Amazon Brasil e retorna o nome e o preço se encontrado.

    Args:
        nome_produto (str): O nome do produto a ser pesquisado.

    Returns:
        dict: Um dicionário contendo o nome e o preço do produto se encontrado,
              senão retorna None.
    """

    url = f"https://www.amazon.com.br/s?k={nome_produto.replace(' ', '+')}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Procura por um item com o nome do produto
    produto = soup.find('span', class_='a-size-medium a-color-base a-text-normal')
    if produto is not None:
        nome = produto.text.strip()

        # Procura pelo preço
        preco = soup.find('span', class_='a-offscreen')
        if preco is not None:
            preco = preco.text.strip()
            return {'nome': nome, 'preco': preco}

    return None

# Exemplo de uso
nome_produto = "controle xbox series x/s com cabo"
produto_encontrado = encontrar_produto_amazon(nome_produto)

if produto_encontrado:
    print(f"O produto '{produto_encontrado['nome']}' foi encontrado na Amazon Brasil.")
    print(f"Preço: {produto_encontrado['preco']}")
else:
    print(f"O produto '{nome_produto}' não foi encontrado na Amazon Brasil.")