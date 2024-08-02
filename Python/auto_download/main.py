import requests
from bs4 import BeautifulSoup
import os

# URL da página web
url = "http://gedex/INTEROP/WebClient/Documento?doc=9ad7e49b-c451-4ca0-8ae9-d32c4f140aee#"

# Pasta de destino para salvar as imagens
pasta_destino = r"C:\Users\e610098\Desktop\medidores"

# Credenciais de login (substitua pelo seu usuário e senha)
usuario = "E610098"
senha = "30diasnomes=)$"

# Faz a requisição para a página com autenticação básica
resposta = requests.get(url, auth=(usuario, senha))
resposta.raise_for_status()  # Verifica se houve algum erro na requisição

# Analisa o HTML da página com BeautifulSoup
sopa = BeautifulSoup(resposta.content, 'html.parser')

# Encontra todos os links com a classe "lnkVisualizarArquivo"
links_arquivos = sopa.find_all('a', class_='lnkVisualizarArquivo')

# Itera sobre os links encontrados
for link in links_arquivos:
    # Extrai o nome do arquivo do texto do link
    nome_arquivo = link.text.strip()

    # Constrói a URL completa da imagem (assumindo que está no mesmo domínio)
    url_imagem = f"{url}/{nome_arquivo}"

    # Faz a requisição para a URL da imagem
    resposta_imagem = requests.get(url_imagem, auth=(usuario, senha))

    # Verifica se a requisição da imagem foi bem-sucedida (código 200)
    if resposta_imagem.status_code == 200:
        # Constrói o caminho completo para salvar a imagem
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

        # Salva a imagem na pasta de destino
        with open(caminho_arquivo, 'wb') as arquivo:
            arquivo.write(resposta_imagem.content)

        print(f"Imagem '{nome_arquivo}' baixada com sucesso!")
    else:
        print(f"Erro ao baixar a imagem '{nome_arquivo}'. Pulando para o próximo.")