import requests

from requests.auth import HTTPBasicAuth

token = 'x'
organization = 'x'

url = f'https://dev.azure.com/{organization}/_apis/projects?api-version=6.0'

response = requests.get(url, auth=HTTPBasicAuth('', token))

if response.status_code == 200:
    data = response.json()
    sorted_projects = sorted(data['value'], key=lambda x: x['name'])
    with open('projetos.txt', 'w', encoding='utf-8') as file:
        file.write(', '.join(f'"{project["name"]}"' for project in sorted_projects))
    print(f'A lista de projetos foi exportada para "projetos.txt". Total de projetos encontrados: {len(sorted_projects)}')
else:
    print('Falha na solicitação: ', response.status_code)