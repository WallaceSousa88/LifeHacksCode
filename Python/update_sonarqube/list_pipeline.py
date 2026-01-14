import os
import csv
import requests

from requests.auth import HTTPBasicAuth

token = os.getenv("AZURE_TOKEN")
organization = os.getenv("AZURE_ORG")

session = requests.Session()
session.auth = HTTPBasicAuth('', token)

def get_projects():
    url = f'https://dev.azure.com/{organization}/_apis/projects?api-version=6.0'
    response = session.get(url)
    if response.ok:
        data = response.json()
        return sorted(data['value'], key=lambda x: x['name'])
    else:
        raise Exception(f"Erro {response.status_code}: {response.text}")

def get_pipelines(project_name):
    url = f'https://dev.azure.com/{organization}/{project_name}/_apis/pipelines?api-version=6.0'
    response = session.get(url)
    if response.ok:
        return response.json()['value']
    else:
        return []

def main():
    projects = get_projects()
    total_pipelines = 0
    with open('pipelines.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Projeto", "Número de Pipelines", "Nomes dos Pipelines"])
        for project in projects:
            pipelines = get_pipelines(project["name"])
            num_pipelines = len(pipelines)
            total_pipelines += num_pipelines
            pipeline_names = "; ".join([p["name"] for p in pipelines])
            writer.writerow([project["name"], num_pipelines, pipeline_names])
        writer.writerow([])
        writer.writerow(["Total de pipelines", total_pipelines])
    print(f'Total de projetos: {len(projects)}. Total de pipelines: {total_pipelines}.')

if __name__ == "__main__":
    main()