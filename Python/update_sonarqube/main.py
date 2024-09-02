from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.exceptions import AzureDevOpsServiceError

personal_access_token = 'x'
organization_url = 'x'

credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
build_client = connection.clients.get_build_client()

with open('projetos.txt', 'r') as file:
    project_names = file.read().strip().split(', ')

altered_projects = set()
failed_projects = set()

for project_name in project_names:
    definitions = build_client.get_definitions(project=project_name)

    for definition in definitions:
        build_definition = build_client.get_definition(definition_id=definition.id, project=project_name)
        altered = False
        try:
            if 'phases' in build_definition.process:
                for phase in build_definition.process['phases']:
                    for step in phase['steps']:
                        if step['displayName'] in ['Prepare analysis on SonarQube', 'Run Code Analysis', 'Publish Quality Gate Result']:
                            step['task']['versionSpec'] = '6.*'
                            step['enabled'] = True
                            altered = True
                        if step['displayName'] == 'Run Code Analysis':
                            step['inputs']['jdkversion'] = 'Use JAVA_HOME'
                            altered = True
            if altered:
                build_client.update_definition(definition=build_definition, definition_id=definition.id, project=project_name)
                altered_projects.add((project_name, f"x{project_name}/_build?definitionId={definition.id}"))
        except AzureDevOpsServiceError:
            failed_projects.add((project_name, f"x{project_name}/_build?definitionId={definition.id}"))

with open('projetos_alterados.txt', 'w') as file:
    file.write("Projeto\tPipeline URL\n")
    for project in altered_projects:
        file.write(f"{project[0]}\t{project[1]}\n")

with open('projetos_erro.txt', 'w') as file:
    file.write("Projeto\tPipeline URL\n")
    for project in failed_projects:
        file.write(f"{project[0]}\t{project[1]}\n")
