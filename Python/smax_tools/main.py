import requests
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

smax_url = config['smax_url']
tenant_id = config['tenant_id']
usuario = config['username']
senha = config['password']
azure_pat = config['azure_pat']

url_login = f"https://{smax_url}/idm-service/idm/v0/login"
url_base_smax = f"https://{smax_url}/rest/{tenant_id}"
url_token_smax = f"{url_base_smax}/auth/authentication-endpoint/authenticate/token"

params_login = {
    "tenant": tenant_id,
    "code": "" ,
    "tryLocal": "true"
}

headers_azure = {
    "Authorization": f"Bearer {azure_pat}"
}

try:
    resposta_login = requests.get(url_login, params=params_login, headers=headers_azure)
    resposta_login.raise_for_status()
    cookies_idm = resposta_login.cookies

    resposta_token_smax = requests.post(url_token_smax, json={"login": usuario, "password": senha}, cookies=cookies_idm)
    resposta_token_smax.raise_for_status()
    token_smax = resposta_token_smax.json()["token"]

    headers_smax = {"SMAX_AUTH_TOKEN": token_smax}
    resposta_teste = requests.get(f"{url_base_smax}/ems/Person", headers=headers_smax)
    resposta_teste.raise_for_status()
    print("Conexão com a API do SMAX estabelecida com sucesso!")

except requests.exceptions.HTTPError as err:
    print(f"Erro na conexão: {err}")

except requests.exceptions.RequestException as err:
    print(f"Erro na conexão: {err}")
