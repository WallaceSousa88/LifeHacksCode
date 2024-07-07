#pip install requests

import requests
from requests.auth import HTTPBasicAuth

pat = 'token'

organization = 'x'

url = f'https://dev.azure.com/{organization}/_apis/projects?api-version=6.0'

response = requests.get(url, auth=HTTPBasicAuth('', pat))

if response.status_code == 200:
    data = response.json()
    sorted_projects = sorted(data['value'], key=lambda x: x['name'])
    with open('projects_list.txt', 'w') as file:
        for index, project in enumerate(sorted_projects, start=1):
            file.write(f'{index}. {project["name"]}\n')
    print('A lista de projetos foi exportada para "projects_list.txt".')
else:
    print('Falha na solicitação: ', response.status_code)
