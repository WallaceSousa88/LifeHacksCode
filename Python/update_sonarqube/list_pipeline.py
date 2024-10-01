import requests

from requests.auth import HTTPBasicAuth

token = 'x'
organization = 'x'

url_projects = f'https://dev.azure.com/{organization}/_apis/projects?api-version=6.0'

response_projects = requests.get(url_projects, auth=HTTPBasicAuth('', token))

if response_projects.status_code == 200:
    data_projects = response_projects.json()
    sorted_projects = sorted(data_projects['value'], key=lambda x: x['name'])

    total_pipelines = 0
    with open('pipelines.txt', 'w', encoding='utf-8') as file:
        for project in sorted_projects:
            project_name = project["name"]
            url_pipelines = f'https://dev.azure.com/{organization}/{project_name}/_apis/pipelines?api-version=6.0'
            response_pipelines = requests.get(url_pipelines, auth=HTTPBasicAuth('', token))
            if response_pipelines.status_code == 200:
                data_pipelines = response_pipelines.json()
                num_pipelines = len(data_pipelines['value'])
                total_pipelines += num_pipelines
                file.write(f'{project_name}, {num_pipelines}\n')
        file.write(f'\nTotal de pipelines em todos os projetos: {total_pipelines}\n')
    print(f'A lista de projetos e o número de pipelines foram exportados para "pipelines.txt". Total de projetos encontrados: {len(sorted_projects)}. Total de pipelines: {total_pipelines}.')
else:
    print('Falha na solicitação: ', response_projects.status_code)