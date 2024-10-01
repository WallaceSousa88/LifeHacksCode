import requests
import json
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

def carregar_configuracoes(nome_arquivo):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    diretorio_pai = os.path.dirname(diretorio_atual)
    caminho_config = os.path.join(diretorio_pai, nome_arquivo)
    with open(caminho_config, 'r') as arquivo:
        return json.load(arquivo)

def carregar_dados_formulario(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        return json.load(arquivo)

def fazer_login(driver, login_url, matricula):
    driver.get(login_url)
    driver.maximize_window()
    username_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "username"))
    )
    username_field.send_keys(matricula)
    time.sleep(3)
    next_button = driver.find_element(By.ID, "next")
    next_button.click()
    time.sleep(10)
    driver.minimize_window()
    cookies = driver.get_cookies()
    return cookies

def enviar_solicitacao(bulk_url, headers, data):
    response = requests.post(bulk_url, headers=headers, json=data)

    if response.status_code == 200:
        print("Solicitação criada com sucesso!\n")
        print(response.json())
    else:
        print(f"Erro ao criar a solicitação. Código: {response.status_code}\n")
        print(response.text)

def main():
    config = carregar_configuracoes('config.json')
    login_url = config['login_url']
    tenant_id = config['tenant_id']
    matricula = config['matricula']
    driver_selenium = config['driver_selenium']
    edge_options = Options()
    service = Service(driver_selenium)
    driver = webdriver.Edge(service=service, options=edge_options)
    cookies = fazer_login(driver, login_url, matricula)
    selenium_cookies = {}
    for cookie in cookies:
        selenium_cookies[cookie['name']] = cookie['value']
    xsrf_token = selenium_cookies['XSRF-TOKEN']
    smax_auth_token = selenium_cookies['SMAX_AUTH_TOKEN']
    bulk_url = f"{login_url}rest/{tenant_id}/ems/bulk"

    print("Escolha uma opção:")
    print("1. Formulário de Reclamação")
    print("2. Formulário de Denúncia")
    print("3. Formulário de Elogio")
    print("4. Formulário de Sugestão")
    print("0. Sair")
    opcao = input("Digite o número da opção desejada: ")

    if opcao == '1':
        nome_arquivo_json = 'form_reclamacao.json'
    elif opcao == '2':
        nome_arquivo_json = 'form_denuncia.json'
    elif opcao == '3':
        nome_arquivo_json = 'form_elogio.json'
    elif opcao == '4':
        nome_arquivo_json = 'form_sugestao.json'
    elif opcao == '0':
        print("Saindo...\n")
        driver.quit()
        exit()
    else:
        print("Opção inválida!\n")
        driver.quit()
        exit()

    dados_formulario = carregar_dados_formulario(nome_arquivo_json)
    form_data = dados_formulario['base']
    data = dados_formulario['data']
    headers = dados_formulario['headers']
    offering_page = data['entities'][0]['properties']['RequestsOffering']
    data['entities'][0]['properties']['UserOptions']['complexTypeProperties'][0]['properties'] = form_data
    data['entities'][0]['properties']['UserOptions'] = json.dumps(data['entities'][0]['properties']['UserOptions'])
    headers['Authorization'] = headers['Authorization'].replace("$smax_auth_token", smax_auth_token)
    headers['X-XSRF-TOKEN'] = headers['X-XSRF-TOKEN'].replace("$xsrf_token", xsrf_token)
    headers['Cookie'] = headers['Cookie'].replace("$cookie_string", '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]))
    headers['x-ui-timestamp'] = headers['x-ui-timestamp'].replace("$timestamp", str(int(time.time() * 1000)))
    headers['origin'] = headers['origin'].replace("$login_url", login_url)
    headers['referer'] = headers['referer'].replace("$referer", f'{login_url}saw/ess/offeringPage/{offering_page}')

    enviar_solicitacao(bulk_url, headers, data)
    time.sleep(3)
    driver.quit()

if __name__ == "__main__":
    main()
